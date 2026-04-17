import datetime as dt
import re
from pathlib import Path

import anthropic

from config import Config


ARTICLE_OUTPUT_RULES = """以下の出力ルールを必ず守ってください。
- 書籍紹介で扱う本は、Amazon.co.jpのKindle版として実在を確信できる日本語書籍のみです。
- 架空の書名、著者名、出版社名、発売日、説明は禁止です。
- Kindleで販売中かつ最新刊だと確認できない場合は、その書籍紹介枠を「該当するKindle書籍を確認できなかったため、このセクションは省略します。」とだけ書いてください。
- 絵文字は禁止です。
- Markdownの水平線、区切り線、表は使わないでください。特に `---` は出力しないでください。
- 出力はMarkdown本文のみとしてください。
"""

EMOJI_PATTERN = re.compile(
    "["  # Common emoji blocks.
    "\U0001F1E6-\U0001F1FF"
    "\U0001F300-\U0001FAFF"
    "\u2700-\u27BF"
    "\u200D"
    "\uFE0F"
    "]+"
)
MARKDOWN_RULE_PATTERN = re.compile(r"^\s*---+\s*$", re.MULTILINE)
MARKDOWN_TABLE_SEPARATOR_PATTERN = re.compile(
    r"^\s*\|?(?:\s*:?-{3,}:?\s*\|)+\s*$",
    re.MULTILINE,
)
HYPHEN_RUN_PATTERN = re.compile(r"-{3,}")


def load_text_file(path: Path) -> str:
    """UTF-8 のテキストファイルを読み込む。

    引数:
        path: 読み込むファイルのパス。

    戻り値:
        str: ファイル内容の文字列。
    """
    return path.read_text(encoding="utf-8")


def load_system_prompt(path: str) -> str:
    """system prompt 用のテキストをファイルから読み込む。

    引数:
        path: system prompt ファイルのパス。

    戻り値:
        str: system prompt の本文。
    """
    return load_text_file(Path(path))


def create_client(config: Config) -> anthropic.Anthropic:
    """設定値を使って Anthropic クライアントを作成する。

    引数:
        config: API キーやモデル設定を保持する設定オブジェクト。

    戻り値:
        anthropic.Anthropic: 初期化済みの Anthropic クライアント。
    """
    if not config.anthropic_api_key:
        raise ValueError("ANTHROPIC_API_KEY is required.")

    return anthropic.Anthropic(api_key=config.anthropic_api_key)


def extract_text_content(message: anthropic.types.Message) -> str:
    """Anthropic のレスポンスからテキスト部分だけを抽出する。

    引数:
        message: Anthropic Messages API のレスポンスオブジェクト。

    戻り値:
        str: テキストブロックを連結した本文。
    """
    response_text = "".join(
        block.text for block in message.content if getattr(block, "type", None) == "text"
    ).strip()
    if not response_text:
        raise ValueError(
            "Anthropic response did not contain any text content.")

    return response_text


def generate_text(
    client: anthropic.Anthropic,
    *,
    system_prompt: str,
    user_prompt: str,
    model: str,
    max_tokens: int,
    temperature: float,
) -> str:
    """Anthropic にプロンプトを送って記事本文を生成する。

    引数:
        client: 利用する Anthropic クライアント。
        system_prompt: system ロールとして渡す指示文。
        user_prompt: user ロールとして渡す入力文。
        model: 使用するモデル名。
        max_tokens: 生成時の最大トークン数。
        temperature: 生成時の温度パラメータ。

    戻り値:
        str: 生成されたテキスト本文。
    """
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
        thinking={"type": "disabled"},
    )
    return extract_text_content(message)


def build_new_user_prompt(instruction: str) -> str:
    """記事生成用ユーザープロンプトに共通ガードレールを追加する。"""
    return (
        f"{ARTICLE_OUTPUT_RULES}\n\n"
        "## 記事生成の指示\n"
        f"{instruction}"
    )


def ensure_output_dir(output_dir: str) -> Path:
    """出力先ディレクトリを必要に応じて作成する。

    引数:
        output_dir: 出力先ディレクトリのパス。

    戻り値:
        Path: 作成または確認済みのディレクトリパス。
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    return output_path


def save_new_output(text: str, output_dir: str) -> Path:
    """新規生成した本文をタイムスタンプ付きファイル名で保存する。

    引数:
        text: 保存する記事本文。
        output_dir: 保存先ディレクトリのパス。

    戻り値:
        Path: 保存したファイルのパス。
    """
    directory = ensure_output_dir(output_dir)
    output_path = directory / \
        f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    output_path.write_text(text, encoding="utf-8")
    return output_path


def normalize_base_stem(path: Path) -> str:
    """編集版サフィックスを除いたベースファイル名を返す。

    引数:
        path: 対象ファイルのパス。

    戻り値:
        str: `_edited_verN` を除いたファイル名。
    """
    return re.sub(r"_edited_ver\d+$", "", path.stem)


def build_edited_output_path(target_path: str, output_dir: str) -> Path:
    """修正版の次回保存先ファイルパスを決定する。

    引数:
        target_path: 修正元ファイルのパス。
        output_dir: 修正版の保存先ディレクトリ。

    戻り値:
        Path: 次のバージョン番号を付けた保存先パス。
    """
    target = Path(target_path)
    directory = ensure_output_dir(output_dir)
    base_stem = normalize_base_stem(target)
    suffix = target.suffix or ".md"
    pattern = re.compile(
        rf"^{re.escape(base_stem)}_edited_ver(\d+){re.escape(suffix)}$")

    versions = []
    for candidate in directory.glob(f"{base_stem}_edited_ver*{suffix}"):
        match = pattern.match(candidate.name)
        if match:
            versions.append(int(match.group(1)))

    next_version = max(versions, default=0) + 1
    return directory / f"{base_stem}_edited_ver{next_version}{suffix}"


def save_edited_output(text: str, target_path: str, output_dir: str) -> Path:
    """修正版本文を次の版番号付きファイル名で保存する。

    引数:
        text: 保存する修正版記事本文。
        target_path: 修正元ファイルのパス。
        output_dir: 保存先ディレクトリのパス。

    戻り値:
        Path: 保存した修正版ファイルのパス。
    """
    output_path = build_edited_output_path(target_path, output_dir)
    output_path.write_text(text, encoding="utf-8")
    return output_path


def sanitize_generated_text(text: str) -> str:
    """禁止している装飾や区切り線を生成結果から除去する。"""
    sanitized = EMOJI_PATTERN.sub("", text)
    sanitized = MARKDOWN_TABLE_SEPARATOR_PATTERN.sub("", sanitized)
    sanitized = MARKDOWN_RULE_PATTERN.sub("", sanitized)
    sanitized = HYPHEN_RUN_PATTERN.sub("--", sanitized)
    sanitized = re.sub(r"\n{3,}", "\n\n", sanitized)
    return sanitized.strip()


def build_edit_user_prompt(existing_text: str, instruction: str) -> str:
    """元記事と修正指示から編集用ユーザープロンプトを組み立てる。

    引数:
        existing_text: 修正対象となる元記事の本文。
        instruction: 反映したい修正指示。

    戻り値:
        str: Anthropic に渡す編集用ユーザープロンプト。
    """
    return (
        f"{ARTICLE_OUTPUT_RULES}\n\n"
        "以下のMarkdown記事をベースに、修正指示を反映した完成版の記事を作成してください。\n"
        "出力は修正後のMarkdown本文のみとしてください。\n\n"
        "## 元記事\n"
        f"{existing_text}\n\n"
        "## 修正指示\n"
        f"{instruction}"
    )
