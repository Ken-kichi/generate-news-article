# To run this code you need to install the following dependencies:
# pip install google-genai

import os
from io import BytesIO
from PIL import Image
from google import genai
from utils import get_summary, generate_thumbnail


def generate():
    """要約抽出とサムネイル生成を一括実行する補助スクリプト。"""

    text = get_summary("output/20260422_090502_edited_ver1.md")

    generate_thumbnail(text, "output")


if __name__ == "__main__":
    generate()
