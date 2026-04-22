# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from io import BytesIO
from PIL import Image
from google import genai
from utils import get_summary, generate_thumbnail


def generate():

    text = get_summary("output/20260422_090502_edited_ver1.md")

    generate_thumbnail(text, "output")

    # # 画像生成の実行（モデル名は随時更新されます）
    # response = client.models.generate_content(
    #     model="gemini-3.1-flash-image-preview",
    #     contents=f"{text}\n\nこの内容をイメージしたnoteのサムネイルを生成してください。"
    # )

    # # 生成された画像データを保存
    # for part in response.candidates[0].content.parts:
    #     if part.inline_data:
    #         image_data = BytesIO(part.inline_data.data)
    #         img = Image.open(image_data)
    #         img.save("generated_image.png")


if __name__ == "__main__":
    generate()
