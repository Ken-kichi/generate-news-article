from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self) -> None:
        self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
        self.anthropic_model = os.getenv("ANTHROPIC_MODEL")
        self.max_evaluation_retries = int(
            os.getenv("MAX_EVALUATION_RETRIES", "2"))
