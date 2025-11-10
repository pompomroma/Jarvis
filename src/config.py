"""Configuration utilities for the multimodal assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _str_to_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


load_dotenv()


@dataclass
class Settings:
    """Runtime settings resolved from the environment."""

    api_key: str | None = os.getenv("OPENAI_API_KEY")
    model_name: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    transcription_model: str = os.getenv(
        "OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe"
    )
    tts_voice: str = os.getenv("OPENAI_TTS_VOICE", "alloy")
    tts_audio_format: str = os.getenv("OPENAI_TTS_AUDIO_FORMAT", "wav")
    search_max_results: int = int(os.getenv("SEARCH_MAX_RESULTS", "3"))
    allow_web_search: bool = _str_to_bool(os.getenv("ALLOW_WEB_SEARCH"), True)

    def validate(self) -> None:
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Provide your project API key via environment variable or .env file."
            )


settings = Settings()
