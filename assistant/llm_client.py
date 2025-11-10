"""Wrapper around the OpenAI client for chat, transcription, and TTS."""

from __future__ import annotations

from typing import Iterable, List, Optional

from openai import OpenAI

from .config import Settings


class LLMClient:
    """High-level client consolidating OpenAI API calls."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = OpenAI(api_key=settings.api_key)

    def chat(
        self,
        messages: Iterable[dict],
        search_snippets: Optional[List[str]] = None,
        temperature: float = 0.7,
    ) -> str:
        """Send conversation context to the chat model and return the assistant reply."""

        inputs: List[dict] = list(messages)
        if search_snippets:
            context_block = {
                "role": "system",
                "content": (
                    "Here are search snippets you can use if they look relevant:\n"
                    + "\n".join(f"- {snippet}" for snippet in search_snippets)
                ),
            }
            inputs.insert(1, context_block)

        response = self._client.responses.create(
            model=self.settings.chat_model,
            temperature=temperature,
            input=list(inputs),
        )

        return response.output_text or ""

    def transcribe(self, audio_path: str) -> str:
        """Transcribe audio from disk using the configured speech-to-text model."""

        with open(audio_path, "rb") as audio_file:
            transcript = self._client.audio.transcriptions.create(
                model=self.settings.transcribe_model,
                file=audio_file,
            )
        return transcript.text

    def synthesize_speech_to_file(self, text: str, output_path: str) -> str:
        """Generate spoken audio for text and write it to ``output_path``."""

        with self._client.audio.speech.with_streaming_response.create(
            model=self.settings.speech_model,
            voice=self.settings.tts_voice,
            input=text,
            format="wav",
        ) as response:
            response.stream_to_file(output_path)
        return output_path
