import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Automatically load environment variables from a .env file if present
load_dotenv()


@dataclass
class Settings:
    """Runtime configuration for the multimodal assistant."""

    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    model: str = field(default_factory=lambda: os.getenv("OPENAI_RESPONSES_MODEL", "gpt-4o-mini"))
    tts_voice: str = field(default_factory=lambda: os.getenv("OPENAI_TTS_VOICE", "alloy"))
    enable_tts: bool = field(default_factory=lambda: os.getenv("ENABLE_TTS", "true").lower() in {"1", "true", "yes"})
    enable_auto_search: bool = field(default_factory=lambda: os.getenv("ENABLE_AUTO_SEARCH", "true").lower() in {"1", "true", "yes"})
    search_confidence_threshold: float = field(
        default_factory=lambda: float(os.getenv("SEARCH_CONFIDENCE_THRESHOLD", "0.6"))
    )
    max_search_results: int = field(default_factory=lambda: int(os.getenv("MAX_SEARCH_RESULTS", "3")))
    local_memory_path: Optional[Path] = field(
        default_factory=lambda: Path(os.getenv("LOCAL_MEMORY_PATH", "knowledge/seed.txt"))
    )


def get_settings() -> Settings:
    """Return validated settings, ensuring the OpenAI API key is present."""
    settings = Settings()
    if not settings.openai_api_key:
        raise RuntimeError(
            "Missing OpenAI API key. Set the OPENAI_API_KEY environment variable or create a .env file with it."
        )
    return settings
