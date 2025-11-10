import argparse
import sys
from typing import Optional

from src.assistant.audio_io import record_microphone
from src.assistant.search import SearchUnavailable, TavilySearchClient, format_results
from src.assistant.service import MultimodalAssistant
from src.config import get_settings


def build_search_client() -> Optional[TavilySearchClient]:
    try:
        return TavilySearchClient()
    except SearchUnavailable as exc:
        print(f"[info] Web search disabled: {exc}")
        return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Multimodal AI assistant (text + voice).")
    parser.add_argument(
        "--voice",
        action="store_true",
        help="Capture microphone input each turn and transcribe it automatically.",
    )
    parser.add_argument(
        "--speak",
        action="store_true",
        help="Enable text-to-speech playback for assistant replies.",
    )
    parser.add_argument(
        "--force-search",
        action="store_true",
        help="Always run a web search before responding.",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=8.0,
        help="Maximum microphone capture length per turn (seconds).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        settings = get_settings()
    except RuntimeError as exc:
        print(exc)
        return 1

    search_client = build_search_client()
    assistant = MultimodalAssistant(settings=settings, search_client=search_client)

    print("Multimodal assistant ready. Type 'quit' or 'exit' to stop.")
    if args.voice:
        print("Voice input enabled. Speak after the prompt.")

    while True:
        if args.voice:
            audio_path = record_microphone(duration_seconds=args.duration)
            user_prompt = assistant.transcribe_audio(audio_path)
            print(f"You (transcribed): {user_prompt}")
        else:
            try:
                user_prompt = input("You: ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nSession terminated.")
                break

        if user_prompt.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break
        if not user_prompt:
            continue

        response = assistant.reply(
            user_prompt=user_prompt,
            speak=args.speak or args.voice,
            force_search=args.force_search,
        )

        print(f"Assistant: {response.text}\n")

        if response.used_search and response.search_results:
            print("Sources:")
            print(format_results(response.search_results))
            print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
