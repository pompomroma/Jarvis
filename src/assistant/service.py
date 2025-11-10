from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from openai import OpenAI

from src.assistant.audio_io import play_audio_file, save_tts_to_file
from src.assistant.local_memory import load_local_memory
from src.assistant.search import SearchResult, TavilySearchClient, format_results
from src.config import Settings


@dataclass
class AssistantResponse:
    text: str
    audio_path: Optional[Path] = None
    used_search: bool = False
    search_results: List[SearchResult] = field(default_factory=list)


class MultimodalAssistant:
    """Coordinates conversation, optional web search, and text-to-speech synthesis."""

    def __init__(self, settings: Settings, search_client: Optional[TavilySearchClient] = None):
        self.settings = settings
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.search_client = search_client
        self.local_memory = load_local_memory(settings.local_memory_path)
        self.history: List[Dict] = []

    # ------------------------------------------------------------------ #
    # Core conversation loop
    # ------------------------------------------------------------------ #
    def reply(
        self,
        user_prompt: str,
        speak: bool = False,
        force_search: bool = False,
    ) -> AssistantResponse:
        """Generate a reply to the provided prompt, optionally speaking the result."""
        search_results: List[SearchResult] = []
        used_search = False

        if self._should_search(user_prompt) or force_search:
            if self.search_client:
                try:
                    search_results = self.search_client.search(
                        user_prompt, max_results=self.settings.max_search_results
                    )
                    used_search = bool(search_results)
                except Exception as exc:  # pragma: no cover - network failure path
                    print(f"[warn] Search failed: {exc}")
            else:
                print("[info] Search requested but no search client configured.")

        response_text = self._generate_response_text(user_prompt, search_results)
        tts_path: Optional[Path] = None

        if speak and self.settings.enable_tts:
            tts_path = self._synthesize_speech(response_text)
            if tts_path:
                play_audio_file(tts_path)

        # Append to conversation memory
        self.history.append({"role": "user", "content": [{"type": "text", "text": user_prompt}]})
        self.history.append({"role": "assistant", "content": [{"type": "text", "text": response_text}]})

        return AssistantResponse(
            text=response_text,
            audio_path=tts_path,
            used_search=used_search,
            search_results=search_results,
        )

    # ------------------------------------------------------------------ #
    # Speech utilities
    # ------------------------------------------------------------------ #
    def transcribe_audio(self, audio_path: Path) -> str:
        """Use Whisper via OpenAI to transcribe a local audio file."""
        with audio_path.open("rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file,
                response_format="text",
            )
        return transcription.strip()

    def _synthesize_speech(self, text: str) -> Optional[Path]:
        """Convert assistant text into speech and store it on disk."""
        if not text.strip():
            return None
        response = self.client.audio.speech.create(
            model="gpt-4o-mini-tts",
            voice=self.settings.tts_voice,
            input=text,
            audio_format="wav",
        )
        audio_bytes = response.read()
        return save_tts_to_file(audio_bytes, suffix=".wav")

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #
    def _should_search(self, prompt: str) -> bool:
        if not self.settings.enable_auto_search:
            return False

        keywords = {
            "news",
            "current",
            "today",
            "latest",
            "update",
            "price",
            "weather",
            "stock",
            "score",
            "trend",
            "breaking",
            "headline",
            "report",
        }
        prompt_lower = prompt.lower()
        score = 0

        for keyword in keywords:
            if keyword in prompt_lower:
                score += 0.2
        if any(token.isdigit() and len(token) == 4 for token in prompt_lower.split()):
            score += 0.2  # likely referencing a year or date

        score = min(score, 1.0)
        return score >= self.settings.search_confidence_threshold

    def _generate_response_text(self, user_prompt: str, search_results: List[SearchResult]) -> str:
        """Call the OpenAI Responses API to get assistant output."""
        search_context = ""
        if search_results:
            search_context = (
                "Web search results:\n"
                f"{format_results(search_results)}\n"
                "When referencing these results, cite them by their number."
            )

        system_prompt = self._build_system_prompt()

        inputs: List[Dict] = [
            {"role": "system", "content": [{"type": "text", "text": system_prompt}]},
        ]
        if search_context:
            inputs.append({"role": "system", "content": [{"type": "text", "text": search_context}]})

        inputs.extend(self.history)

        inputs.append(
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                ],
            }
        )

        response = self.client.responses.create(
            model=self.settings.model,
            input=inputs,
        )
        return response.output_text.strip()

    def _build_system_prompt(self) -> str:
        base_prompt = (
            "You are a multimodal personal assistant that can respond conversationally in text. "
            "When possible, keep answers grounded in local knowledge. "
            "If web search context is provided, integrate it responsibly and cite sources. "
            "If no search data is available and the user asks for creative content, produce it autonomously."
        )
        if self.local_memory:
            base_prompt += f"\n\nLocal memory:\n{self.local_memory}"
        return base_prompt
