"""Entry point for the multimodal AI assistant."""

from __future__ import annotations

import argparse

from assistant.config import Settings
from assistant.orchestrator import AssistantOrchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multimodal AI assistant with text, voice, and optional web search."
    )
    parser.add_argument(
        "--mode",
        choices=("text", "voice"),
        default="text",
        help="Run in text-only chat mode or voice-enabled mode.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = Settings.from_env()
    orchestrator = AssistantOrchestrator(settings)

    if args.mode == "voice":
        orchestrator.voice_session()
    else:
        orchestrator.text_session()


if __name__ == "__main__":
    main()
