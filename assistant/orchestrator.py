"""Conversation orchestration for the multimodal AI assistant."""

from __future__ import annotations

import re
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from rich.console import Console
from rich.panel import Panel

from .audio import is_audio_io_available, play_audio_file, record_microphone
from .config import Settings
from .llm_client import LLMClient
from .web_search import search_snippets

console = Console()


SEARCH_TRIGGER_PATTERN = re.compile(
    r"\b(search|look\s*up|latest|news|info(?:rmation)? on)\b", re.IGNORECASE
)


class AssistantOrchestrator:
    """High-level controller handling text and voice conversations."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.client = LLMClient(settings)
        self.history: List[Dict[str, str]] = [
            {
                "role": "system",
                "content": (
                    "You are an adaptive multimodal personal assistant. "
                    "Use embedded knowledge and reasoning to answer questions. "
                    "When the user requests real-world facts or timely updates, "
                    "ask for or leverage search snippets if provided. "
                    "Be concise unless the user explicitly asks for detail."
                ),
            }
        ]

    def reset(self) -> None:
        """Clear the conversation history to start fresh."""

        self.history = self.history[:1]

    def _should_search(self, message: str) -> bool:
        """Determine whether the user input warrants an online search."""

        if message.lower().startswith("search:"):
            return True
        if "no-search" in message.lower():
            return False
        return bool(SEARCH_TRIGGER_PATTERN.search(message))

    def _collect_search_snippets(self, message: str) -> List[str]:
        """Collect search snippets if the message appears to require them."""

        if not self._should_search(message):
            return []

        query = message.replace("search:", "", 1).strip() or message
        snippets = search_snippets(query)
        if snippets:
            console.print(Panel("\n".join(snippets), title="Search snippets", expand=False))
        else:
            console.print("[yellow]No search results were found for that query.[/]")
        return snippets

    def _chat(self, message: str, *, allow_search: bool = True) -> str:
        """Send a user message through the LLM and capture the reply."""

        self.history.append({"role": "user", "content": message})

        snippets: Optional[List[str]] = []
        if allow_search:
            snippets = self._collect_search_snippets(message)

        reply = self.client.chat(self.history, search_snippets=snippets or None)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def text_session(self) -> None:
        """Interactive text session loop."""

        console.print(Panel("Text session started. Type 'exit' to quit.", title="Assistant"))
        while True:
            user_input = console.input("[bold green]You> [/]").strip()
            if user_input.lower() in {"exit", "quit"}:
                console.print("[cyan]Ending session.[/]")
                break
            if user_input.lower() == "reset":
                self.reset()
                console.print("[cyan]Conversation history cleared.[/]")
                continue

            reply = self._chat(user_input)
            console.print(Panel(reply, title="Assistant", expand=False))

    def voice_session(self) -> None:
        """Interactive voice session loop using speech-to-text and TTS."""

        if not is_audio_io_available():
            console.print(
                "[red]Audio devices not detected. Connect a microphone and speaker before starting voice mode.[/]"
            )
            return

        console.print(
            Panel(
                "Voice session started. Press Enter to record, or type 'exit' to quit.",
                title="Assistant Voice Mode",
            )
        )

        while True:
            command = console.input("[bold green]Press Enter to record (or type exit/reset)> [/]")
            if command.strip().lower() in {"exit", "quit"}:
                console.print("[cyan]Ending voice session.[/]")
                break
            if command.strip().lower() == "reset":
                self.reset()
                console.print("[cyan]Conversation history cleared.[/]")
                continue

            console.print(f"[cyan]Recording for up to {self.settings.max_voice_seconds} seconds...[/]")
            with tempfile.TemporaryDirectory() as tmpdir:
                audio_path = Path(tmpdir) / "input.wav"
                record_microphone(
                    audio_path,
                    duration_seconds=float(self.settings.max_voice_seconds),
                )
                console.print("[cyan]Transcribing...[/]")
                transcript = self.client.transcribe(str(audio_path))
            console.print(f"[bold green]You (transcribed)>[/] {transcript}")

            if not transcript.strip():
                console.print("[yellow]No speech detected. Try again.[/]")
                continue

            reply = self._chat(transcript)
            console.print(Panel(reply, title="Assistant", expand=False))

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
                tts_path = self.client.synthesize_speech_to_file(reply, tmpfile.name)
            console.print("[cyan]Playing audio reply...[/]")
            play_audio_file(tts_path)
            Path(tts_path).unlink(missing_ok=True)
