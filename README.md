# generate-news-article

Anthropic APIを使ってMarkdown記事を生成・修正する CLI ツールです。
`python-fire` ベースで `new` と `edit` の 2 コマンドを提供します。

## 必要環境変数

- `ANTHROPIC_API_KEY` (必須)
- `ANTHROPIC_MODEL` (任意。未指定時は `claude-sonnet-4-6`)

`.env` がある場合は自動読み込みします。

## 実行例

```bash
uv run main.py new --prompt="日本のAI業界の最新動向を見出し付きでまとめて"
```

```bash
uv run main.py edit \
  --target=output/20260416_215402.md \
  --prompt="導入文を短くして、見出しをより具体的にしてください"
```

```bash
uv run generate-news-article new --prompt="SaaS市場のニュースを要約"
```

```bash
uv run generate-news-article edit \
  --target=output/20260416_215402.md \
  --prompt="固有名詞の表記を統一してください"
```

## コマンド

- `new`: 新規記事を生成します
- `edit`: `output/` 配下の既存 Markdown をベースに修正版を生成します

## 主なオプション

- `--prompt`: 生成または修正の指示
- `--target`: `edit` 時の対象ファイル
- `--system_prompt_file`: system prompt の Markdown ファイル
- `--output_dir`: 出力先ディレクトリ
- `--model`: 使用モデル
- `--max_tokens`: 最大生成トークン
- `--temperature`: 生成温度

## 出力ファイル名

- `new`: `output/YYYYMMDD_HHMMSS.md`
- `edit`: `output/<元ファイル名>_edited_ver<修正回数>.md`

例:

- 元ファイル: `output/20260416_215402.md`
- 初回修正: `output/20260416_215402_edited_ver1.md`
- 2回目修正: `output/20260416_215402_edited_ver2.md`

## エントリポイント

インストール後は以下でも実行できます。

```bash
generate-news-article new --prompt="生成したい内容"
```
