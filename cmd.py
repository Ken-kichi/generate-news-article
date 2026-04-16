from pathlib import Path
from utils import (
    build_edit_user_prompt,
    save_edited_output,
    load_system_prompt,
    save_new_output,
    create_client,
    generate_text,
    load_text_file
)
from config import Config
from pathlib import Path
from config import Config

conig = Config()


class CLI:
    def __init__(self) -> None:
        """CLI の共有設定を初期化する。

        引数:
            なし

        戻り値:
            なし
        """
        self.config = Config()

    def new(
        self,
        prompt: str,
        system_prompt_file: str = conig.default_system_prompt_path,
        output_dir: str = "output",
        model: str | None = None,
        max_tokens: int = 20000,
        temperature: float = 1.0,
    ) -> str:
        """新規記事を生成して output ディレクトリに保存する。

        引数:
            prompt: 記事生成の指示文。
            system_prompt_file: system prompt を読み込むファイルパス。
            output_dir: 生成結果の保存先ディレクトリ。
            model: 使用する Anthropic モデル名。未指定時は設定値を使う。
            max_tokens: 生成時の最大トークン数。
            temperature: 生成時の温度パラメータ。

        戻り値:
            str: 保存した Markdown ファイルのパス。
        """
        if not prompt.strip():
            raise ValueError("prompt is required.")

        client = create_client(self.config)
        system_prompt = load_system_prompt(system_prompt_file)
        response_text = generate_text(
            client,
            system_prompt=system_prompt,
            user_prompt=prompt,
            model=model or self.config.anthropic_model,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        output_path = save_new_output(response_text, output_dir)
        print(response_text)
        return str(output_path)

    def edit(
        self,
        target: str,
        prompt: str,
        system_prompt_file: str = conig.default_system_prompt_path,
        output_dir: str = "output",
        model: str | None = None,
        max_tokens: int = 20000,
        temperature: float = 1.0,
    ) -> str:
        """既存記事をもとに修正版を生成して保存する。

        引数:
            target: 修正対象となる既存 Markdown ファイルのパス。
            prompt: 記事修正の指示文。
            system_prompt_file: system prompt を読み込むファイルパス。
            output_dir: 修正版の保存先ディレクトリ。
            model: 使用する Anthropic モデル名。未指定時は設定値を使う。
            max_tokens: 生成時の最大トークン数。
            temperature: 生成時の温度パラメータ。

        戻り値:
            str: 保存した修正版 Markdown ファイルのパス。
        """
        target_path = Path(target)
        if not target_path.exists():
            raise FileNotFoundError(f"Target file not found: {target}")
        if not prompt.strip():
            raise ValueError("prompt is required.")

        client = create_client(self.config)
        system_prompt = load_system_prompt(system_prompt_file)
        existing_text = load_text_file(target_path)
        user_prompt = build_edit_user_prompt(existing_text, prompt)
        response_text = generate_text(
            client,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            model=model or self.config.anthropic_model,
            max_tokens=max_tokens,
            temperature=temperature,
        )
        output_path = save_edited_output(response_text, target, output_dir)
        print(response_text)
        return str(output_path)
