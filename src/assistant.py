#!/usr/bin/env python3
"""Multimodal AI assistant supporting text + voice I/O with optional web search."""

from __future__ import annotations

import os
import queue
import sys
import tempfile
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from dotenv import load_dotenv
import simpleaudio as sa
import sounddevice as sd
import soundfile as sf
from duckduckgo_search import DDGS
from openai import OpenAI
from openai.error import OpenAIError


@dataclass
class AssistantConfig:
    """Runtime configuration for the multimodal assistant."""

    model: str = "gpt-4o-mini"
    transcription_model: str = "gpt-4o-mini-transcribe"
    tts_model: str = "gpt-4o-mini-tts"
    voice: str = "alloy"
    system_prompt: str = (
        "You are a helpful multimodal personal assistant."
        " Respond concisely and factually."
        " When web search context is provided, cite it naturally in your answer."
        " If no web data is available, answer from your own knowledge without referring to the web."
    )
    temperature: float = 0.7
    max_response_tokens: int = 600
    max_history_turns: int = 8
    sample_rate: int = 16_000
    max_record_seconds: Optional[int] = 45
    auto_play_audio: bool = True
    minimum_voice_seconds: float = 1.0
    search_results: int = 5


class VoiceAssistant:
    """Interactive assistant orchestrating text and voice workflows."""

    def __init__(self, config: AssistantConfig) -> None:
        self.config = config
        self.history: List[Dict[str, str]] = []
        self.client = OpenAI()
        self._ensure_audio_devices()

    def _ensure_audio_devices(self) -> None:
        try:
            sd.query_devices()
        except Exception as exc:  # pragma: no cover - defensive
            raise RuntimeError(
                "Could not access audio devices. Ensure a microphone and speakers are available"
            ) from exc

    # ------------------------------------------------------------------
    # Audio capture and playback helpers
    # ------------------------------------------------------------------
    def record_voice(self, output_path: Path) -> Optional[Path]:
        """Record from default microphone until Enter is pressed or timeout occurs."""

        q: "queue.Queue" = queue.Queue()
        stop_event = threading.Event()

        def _on_audio(indata, frames, time_info, status):  # pragma: no cover - relies on hardware
            if status:
                print(f"[voice-warning] {status}", file=sys.stderr)
            q.put(indata.copy())

        def _stopper():
            try:
                input("Press Enter to stop recording... ")
            except EOFError:
                pass
            stop_event.set()

        stopper_thread = threading.Thread(target=_stopper, daemon=True)
        stopper_thread.start()

        timer: Optional[threading.Timer] = None
        if self.config.max_record_seconds:
            def _timeout():
                print("\n[info] Auto-stopping recorder after timeout.")
                stop_event.set()

            timer = threading.Timer(self.config.max_record_seconds, _timeout)
            timer.start()

        print("Listening... start speaking.")
        frames_written = 0
        try:
            with sd.InputStream(
                samplerate=self.config.sample_rate,
                channels=1,
                callback=_on_audio,
            ):
                with sf.SoundFile(
                    output_path,
                    mode="w",
                    samplerate=self.config.sample_rate,
                    channels=1,
                ) as audio_file:
                    while True:
                        if stop_event.is_set() and q.empty():
                            break
                        try:
                            data = q.get(timeout=0.2)
                        except queue.Empty:
                            continue
                        audio_file.write(data)
                        frames_written += len(data)
        except KeyboardInterrupt:  # pragma: no cover - interactive
            print("\n[info] Recording interrupted by user.")
            stop_event.set()
        finally:
            if timer:
                timer.cancel()
            stopper_thread.join(timeout=0.2)

        duration = frames_written / float(self.config.sample_rate)
        if duration < self.config.minimum_voice_seconds:
            print("[warn] Captured audio is too short; please try again.")
            return None

        print(f"Recorded {duration:.1f} seconds of audio.")
        return output_path

    def transcribe(self, audio_path: Path) -> Optional[str]:
        try:
            with audio_path.open("rb") as audio_file:
                result = self.client.audio.transcriptions.create(
                    model=self.config.transcription_model,
                    file=audio_file,
                )
        except OpenAIError as exc:
            print(f"[error] Transcription failed: {exc}")
            return None

        text = result.text.strip()
        if not text:
            print("[warn] Transcription returned empty text.")
            return None
        return text

    def speak(self, text: str) -> None:
        print(f"Assistant: {text}\n")
        if not self.config.auto_play_audio:
            return
        try:
            with self.client.audio.speech.with_streaming_response.create(
                model=self.config.tts_model,
                voice=self.config.voice,
                input=text,
                format="wav",
            ) as response:
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    temp_path = Path(tmp_file.name)
                    response.stream_to_file(temp_path)
        except OpenAIError as exc:
            print(f"[warn] Text-to-speech failed: {exc}")
            return
        except Exception as exc:  # pragma: no cover - file system/audio specific
            print(f"[warn] Could not play audio: {exc}")
            return

        try:
            wave_obj = sa.WaveObject.from_wave_file(str(temp_path))
            play_obj = wave_obj.play()
            play_obj.wait_done()
        finally:
            try:
                temp_path.unlink()
            except FileNotFoundError:
                pass

    # ------------------------------------------------------------------
    # Conversation + search
    # ------------------------------------------------------------------
    def maybe_extract_search(self, text: str) -> Tuple[str, Optional[str]]:
        lowered = text.strip().lower()
        prefixes = ["search:", "search for", "web search:"]
        for prefix in prefixes:
            if lowered.startswith(prefix):
                query = text[len(prefix):].strip()
                return "", query or None
        return text, None

    def search_web(self, query: str) -> List[Dict[str, str]]:
        print(f"[info] Searching the web for: {query}")
        results: List[Dict[str, str]] = []
        try:
            with DDGS() as ddgs:
                for idx, result in enumerate(
                    ddgs.text(query, max_results=self.config.search_results)
                ):
                    results.append(
                        {
                            "title": result.get("title", "(untitled)"),
                            "href": result.get("href", ""),
                            "body": result.get("body", ""),
                        }
                    )
                    if idx + 1 >= self.config.search_results:
                        break
        except Exception as exc:  # pragma: no cover - network specific
            print(f"[warn] Web search failed: {exc}")
        return results

    def _format_search_context(self, results: List[Dict[str, str]]) -> str:
        lines = ["Web search findings:"]
        for idx, item in enumerate(results, start=1):
            lines.append(f"{idx}. {item['title']} - {item['href']}")
            if item["body"]:
                lines.append(f"   {item['body']}")
        return "\n".join(lines)

    def generate_response(
        self, user_text: str, search_results: Optional[List[Dict[str, str]]] = None
    ) -> str:
        messages: List[Dict[str, str]] = [{"role": "system", "content": self.config.system_prompt}]
        messages.extend(self.history[-(self.config.max_history_turns * 2) :])
        if search_results:
            messages.append(
                {
                    "role": "system",
                    "content": self._format_search_context(search_results),
                }
            )
        messages.append({"role": "user", "content": user_text})

        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_response_tokens,
            )
        except OpenAIError as exc:
            raise RuntimeError(f"OpenAI chat request failed: {exc}") from exc

        reply = response.choices[0].message.content.strip()
        self.history.append({"role": "user", "content": user_text})
        self.history.append({"role": "assistant", "content": reply})
        # Trim history to configured limit
        excess = len(self.history) - (self.config.max_history_turns * 2)
        if excess > 0:
            self.history = self.history[excess:]
        return reply

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self) -> None:
        print("Multimodal AI Assistant")
        print("Type your question or enter 'v' to use voice input. Enter 'q' to quit.\n")
        while True:
            try:
                user_choice = input("[t]ext, [v]oice, [q]uit > ").strip().lower()
            except EOFError:
                print("\n[info] Received EOF: exiting.")
                break

            if user_choice in {"q", "quit", "exit"}:
                print("Goodbye!")
                break

            if user_choice not in {"t", "text", "v", "voice"}:
                print("Please enter 't' for text, 'v' for voice, or 'q' to quit.")
                continue

            if user_choice.startswith("v"):
                text = self._handle_voice_interaction()
            else:
                text = self._handle_text_interaction()

            if not text:
                continue

            cleaned_text, search_query = self.maybe_extract_search(text)
            search_results = self.search_web(search_query) if search_query else None

            try:
                reply = self.generate_response(cleaned_text or text, search_results)
            except RuntimeError as exc:
                print(f"[error] {exc}")
                continue

            self.speak(reply)

    def _handle_text_interaction(self) -> Optional[str]:
        text = input("You: ").strip()
        if not text:
            print("[warn] Empty input ignored.")
            return None
        return text

    def _handle_voice_interaction(self) -> Optional[str]:
        tmp_dir = Path.cwd() / "temp"
        tmp_dir.mkdir(exist_ok=True)
        audio_path = tmp_dir / f"voice_{int(time.time()*1000)}.wav"

        recorded_path = self.record_voice(audio_path)
        if not recorded_path:
            try:
                audio_path.unlink()
            except FileNotFoundError:
                pass
            return None

        transcription = self.transcribe(recorded_path)
        try:
            recorded_path.unlink()
        except FileNotFoundError:
            pass

        if transcription:
            print(f"You (voice): {transcription}")
        return transcription


def main() -> None:
    load_dotenv()
    if not os.getenv("OPENAI_API_KEY"):
        print("[error] OPENAI_API_KEY is not set. Add it to your environment or .env file.")
        sys.exit(1)

    config = AssistantConfig()
    assistant = VoiceAssistant(config)
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n[info] Session interrupted. Bye!")


if __name__ == "__main__":
    main()
