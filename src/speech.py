"""Utilities for capturing microphone input and playing audio responses."""

from __future__ import annotations

import contextlib
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import simpleaudio as sa
import sounddevice as sd
from scipy.io.wavfile import write as write_wav


def capture_voice_prompt(
    output_path: Path,
    *,
    duration_seconds: float = 12.0,
    sample_rate: int = 16_000,
) -> Path:
    """Record audio from the default microphone and persist as a WAV file.

    Args:
        output_path: Destination for the WAV audio.
        duration_seconds: Maximum recording length. Adjust as needed.
        sample_rate: Microphone sampling rate.

    Returns:
        Path to the WAV file containing the recorded audio.
    """
    sd.default.samplerate = sample_rate
    sd.default.channels = 1

    print(f"🎤 Recording for up to {duration_seconds:.1f}s... speak now.")
    try:
        audio_frames = sd.rec(
            int(duration_seconds * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
    except Exception as exc:  # sounddevice errors (e.g., missing PortAudio)
        raise RuntimeError(
            "Failed to access the system microphone. Install PortAudio or configure the default input device."
        ) from exc

    if not np.any(audio_frames):
        raise RuntimeError("No audio was captured from the microphone.")

    # Convert to 16-bit PCM WAV
    pcm_audio = np.int16(np.clip(audio_frames, -1.0, 1.0) * 32767)
    with contextlib.suppress(FileNotFoundError):
        output_path.unlink()
    write_wav(output_path, sample_rate, pcm_audio)

    print(f"✅ Saved recording to {output_path}")
    return output_path


def play_audio_file(audio_path: Path) -> None:
    """Play a WAV audio file through the system speakers."""
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    try:
        wave_obj = sa.WaveObject.from_wave_file(str(audio_path))
        play_obj = wave_obj.play()
        play_obj.wait_done()
    except Exception as exc:
        print(
            f"⚠️  Unable to play audio automatically ({exc}). "
            f"You can open {audio_path} manually to listen.",
            file=sys.stderr,
        )


def play_audio_bytes(audio_bytes: bytes, *, temp_path: Optional[Path] = None) -> None:
    """Persist audio bytes to disk (optional) and play them."""
    tmp_path = temp_path or Path.cwd() / "assistant_reply.wav"
    tmp_path.write_bytes(audio_bytes)
    play_audio_file(tmp_path)
