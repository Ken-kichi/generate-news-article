
import datetime as dt
from pathlib import Path
import anthropic
from config import Config


def main():

    config = Config()

    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
        api_key=config.anthropic_api_key,
    )
    # prompt/prompt_ver6.md を読み込む
    with open("prompt/prompt_ver6.md", "r") as f:
        prompt = f.read()

    # 生成する
    message = client.messages.create(
        model=config.anthropic_model,
        max_tokens=20000,
        temperature=1,
        system=prompt,
        messages=[
            {"role": "user", "content": "本はKindleで購入できる最新のものにしてください。"},
        ],
        thinking={
            "type": "disabled"
        }
    )
    response_text = "".join(
        block.text for block in message.content if getattr(block, "type", None) == "text"
    )
    print(response_text)

    # 生成した内容を output/ に保存する YYYYMMDD＿hhmmss.md形式
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / \
        f"{dt.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    with open(output_path, "w") as f:
        f.write(response_text)


if __name__ == "__main__":
    main()
