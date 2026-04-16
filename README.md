# generate-news-article

Anthropic APIを使って、CLIで指定したプロンプトからMarkdownを生成し、
`YYYYMMDD_<prefix>.md` の形式で保存するツールです。

## 必要環境変数

- `ANTHROPIC_API_KEY` (必須)
- `ANTHROPIC_MODEL` (任意。未指定時は `claude-sonnet-4-6`)

`.env` がある場合は自動読み込みします。

## 実行例

```bash
python main.py "日本のAI業界の最新動向を見出し付きでまとめて"
```

```bash
python main.py --prompt "SaaS市場のニュースを要約" --prefix saas_news
```

```bash
python main.py --prompt-file prompt/prompt_ver6.md --prefix zenn_draft
```

```bash
python main.py --prompt "テスト" --dry-run --prefix sample
```

## 主なオプション

- `prompt` / `--prompt`: プロンプト本文
- `--prompt-file`: プロンプトファイル
- `--prefix`: ファイル名サフィックス (`YYYYMMDD_<prefix>.md`)
- `--output-dir`: 出力先ディレクトリ
- `--model`: 使用モデル
- `--max-tokens`: 最大生成トークン
- `--temperature`: 生成温度
- `--dry-run`: APIを呼ばずにファイルのみ作成

## エントリポイント

インストール後は以下でも実行できます。

```bash
generate-news-article --prompt "生成したい内容"
```
