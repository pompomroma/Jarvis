"""Configuration helpers for the AI assistant."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    """Application settings loaded from environment variables."""

    api_key: str
    chat_model: str = "gpt-4o-mini"
    speech_model: str = "gpt-4o-mini-tts"
    transcribe_model: str = "gpt-4o-transcribe"
    max_voice_seconds: int = 12
    tts_voice: str = "alloy"

    @classmethod
    def from_env(cls) -> "Settings":
        """Load configuration values from environment variables."""

        load_dotenv(override=False)

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "Missing OPENAI_API_KEY. Create a .env file or set the environment variable."
            )

        chat_model = os.getenv("DEFAULT_MODEL", cls.chat_model)
        speech_model = os.getenv("SPEECH_MODEL", cls.speech_model)
        transcribe_model = os.getenv("TRANSCRIBE_MODEL", cls.transcribe_model)
        max_voice_seconds = int(os.getenv("MAX_VOICE_RECORD_SECONDS", cls.max_voice_seconds))
        tts_voice = os.getenv("TTS_VOICE", cls.tts_voice)

        return cls(
            api_key=api_key,
            chat_model=chat_model,
            speech_model=speech_model,
            transcribe_model=transcribe_model,
            max_voice_seconds=max_voice_seconds,
            tts_voice=tts_voice,
        )
