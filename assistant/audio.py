"""Audio utilities for recording microphone input and playing speech."""

from __future__ import annotations

from pathlib import Path
import sounddevice as sd
import soundfile as sf


def record_microphone(
    output_path: str | Path,
    *,
    duration_seconds: float,
    sample_rate: int = 16_000,
    channels: int = 1,
) -> Path:
    """Record audio from the default microphone."""

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    frames = int(duration_seconds * sample_rate)
    recording = sd.rec(frames, samplerate=sample_rate, channels=channels, dtype="float32")
    sd.wait()

    sf.write(output, recording, sample_rate)
    return output


def play_audio_file(path: str | Path) -> None:
    """Play an audio file using the default output device."""

    data, sample_rate = sf.read(path, dtype="float32")
    sd.play(data, sample_rate)
    sd.wait()


def is_audio_io_available() -> bool:
    """Return True if input and output audio devices appear available."""

    try:
        sd.check_input_settings()
        sd.check_output_settings()
    except Exception:
        return False
    return True
