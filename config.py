import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self) -> None:
        """環境変数から実行時設定を読み込む。

        引数:
            なし

        戻り値:
            なし
        """
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_model = os.getenv(
            "ANTHROPIC_MODEL", "claude-sonnet-4-6")
        self.max_evaluation_retries = int(
            os.getenv("MAX_EVALUATION_RETRIES", "2"))
        self.default_system_prompt_path = os.getenv(
            "DEFAULT_SYSTEM_PROMPT_PATH", "prompt/prompt_ver6.md")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
