"""Core multimodal assistant orchestration."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Optional

from openai import OpenAI

from .config import settings
from .search import format_search_results, run_web_search
from .speech import capture_voice_prompt, play_audio_file


class MultimodalAssistant:
    """Wrapper around the OpenAI APIs for text, voice, and search."""

    def __init__(self) -> None:
        settings.validate()
        self.client = OpenAI(api_key=settings.api_key)
        self.model_name = settings.model_name
        self.transcription_model = settings.transcription_model
        self.tts_voice = settings.tts_voice
        self.tts_audio_format = settings.tts_audio_format
        self.allow_web_search = settings.allow_web_search
        self.search_max_results = settings.search_max_results

        self._history: list[dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are Jarvis, an attentive, multimodal personal assistant. "
                    "You can reason about requests, answer creatively, and clearly explain your thinking. "
                    "Leverage web search results when they are provided, but you can also respond from your own knowledge "
                    "without searching when the task does not require external information."
                ),
            }
        ]

    # ---------------------------------------------------------------------#
    # Conversation helpers
    # ---------------------------------------------------------------------#
    def ask(
        self,
        prompt: str,
        *,
        use_web: Optional[bool] = None,
    ) -> str:
        """Send a text prompt to the assistant and return its text reply."""
        prompt = prompt.strip()
        if not prompt:
            raise ValueError("Prompt must not be empty.")

        should_search = self.allow_web_search if use_web is None else use_web
        messages = list(self._history)
        if should_search:
            results = run_web_search(prompt, max_results=self.search_max_results)
            search_summary = format_search_results(results)
            messages.append(
                {
                    "role": "system",
                    "content": (
                        f"Recent web search for '{prompt}':\n{search_summary}\n"
                        "You may cite these results if they are directly relevant."
                    ),
                }
            )

        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=messages,
        )
        message = response.choices[0].message
        text_reply = message.content or ""

        self._history.extend(
            [
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": text_reply},
            ]
        )

        # Trim history if it grows too large (memory safety)
        if len(self._history) > 40:
            # Keep system prompt and last 39 exchanges
            system_prompt = self._history[0]
            self._history = [system_prompt] + self._history[-39:]

        return text_reply

    # ---------------------------------------------------------------------#
    # Audio input/output utilities
    # ---------------------------------------------------------------------#
    def record_voice_prompt(self, *, duration_seconds: float = 12.0) -> str:
        """Record a voice prompt, transcribe it, and return the resulting text."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            audio_path = Path(tmp_dir) / "voice_prompt.wav"
            capture_voice_prompt(
                audio_path,
                duration_seconds=duration_seconds,
                sample_rate=16_000,
            )
            transcription = self.transcribe_audio(audio_path)
        return transcription

    def transcribe_audio(self, audio_path: Path) -> str:
        """Transcribe a WAV audio file into text."""
        with audio_path.open("rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model=self.transcription_model,
                file=audio_file,
            )
        return response.text.strip()

    def synthesize_speech(self, text: str, output_path: Optional[Path] = None) -> Path:
        """Convert assistant text into speech and write it to disk."""
        text = text.strip()
        if not text:
            raise ValueError("Cannot synthesize empty text.")

        if output_path is None:
            output_path = Path.cwd() / "assistant_reply.wav"

        with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=self.tts_voice,
            input=text,
            format=self.tts_audio_format,
        ) as stream:
            stream.stream_to_file(str(output_path))
        return output_path

    def speak(self, text: str) -> Path:
        """Generate speech for the provided text and play it immediately."""
        audio_path = self.synthesize_speech(text)
        play_audio_file(audio_path)
        return audio_path

    def speak_inline(self, text: str) -> None:
        """Generate speech without leaving residual files."""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            output_path = Path(tmp.name)
        audio_path = self.synthesize_speech(text, output_path=output_path)
        play_audio_file(audio_path)
        audio_path.unlink(missing_ok=True)


# -------------------------------------------------------------------------#
# CLI helper
# -------------------------------------------------------------------------#
def run_cli_loop() -> None:
    """Interactive command-line session for the assistant."""
    assistant = MultimodalAssistant()

    print("🤖 Multimodal Jarvis assistant ready.")
    print("Type a message, or enter '/voice' to record speech, '/quit' to exit.")
    print("Use '/voice web' to trigger a voice prompt with web search.")

    while True:
        user_input = input("\nYou> ").strip()
        if not user_input:
            continue

        if user_input.lower() in {"/quit", "/exit"}:
            print("👋 Goodbye!")
            break

        if user_input.startswith("/voice"):
            use_web = "web" in user_input.lower()
            try:
                prompt_text = assistant.record_voice_prompt()
                print(f"[Voice prompt transcribed]: {prompt_text}")
            except Exception as exc:
                print(f"⚠️  Voice capture failed: {exc}")
                continue
            reply = assistant.ask(prompt_text, use_web=use_web)
        else:
            use_web = user_input.endswith(" --web")
            prompt = user_input[:-6].strip() if use_web else user_input
            reply = assistant.ask(prompt, use_web=use_web)

        print(f"Jarvis> {reply}")

        try:
            assistant.speak_inline(reply)
        except Exception as exc:
            print(f"⚠️  Could not play voice reply automatically ({exc}).")


__all__ = ["MultimodalAssistant", "run_cli_loop"]
