import tempfile
from pathlib import Path
from typing import Optional

import numpy as np
import simpleaudio as sa
import sounddevice as sd
import soundfile as sf


def record_microphone(duration_seconds: float = 10.0, sample_rate: int = 16_000) -> Path:
    """
    Capture audio from the default microphone and store it as a temporary WAV file.

    Parameters
    ----------
    duration_seconds
        Maximum recording length. The capture stops automatically when the duration elapses.
    sample_rate
        Sampling rate in Hz. Whisper performs well with 16 kHz audio.

    Returns
    -------
    Path to the recorded WAV file on disk.
    """
    if duration_seconds <= 0:
        raise ValueError("Recording duration must be greater than zero seconds.")

    print(f"[mic] Recording for up to {duration_seconds} second(s)...")
    frames = int(duration_seconds * sample_rate)
    recording = sd.rec(frames, samplerate=sample_rate, channels=1, dtype=np.float32)
    sd.wait()  # Block until recording is finished
    print("[mic] Recording complete.")

    audio_path = Path(tempfile.mkstemp(suffix=".wav")[1])
    sf.write(audio_path, recording, sample_rate)
    return audio_path


def play_audio_file(audio_path: Path) -> None:
    """
    Play an audio file (expected WAV) using the system's default output device.
    """
    if not audio_path.exists():
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    data, sample_rate = sf.read(audio_path, dtype="float32")
    # simpleaudio expects int16; convert accordingly.
    audio_int16 = np.int16(data * 32767)
    num_channels = 1 if audio_int16.ndim == 1 else audio_int16.shape[1]
    play_obj = sa.play_buffer(audio_int16.tobytes(), num_channels, 2, sample_rate)
    play_obj.wait_done()


def save_tts_to_file(audio_bytes: bytes, output_path: Optional[Path] = None, suffix: str = ".wav") -> Path:
    """
    Persist the raw audio bytes returned from the OpenAI TTS API to disk.
    """
    if output_path is None:
        output_path = Path(tempfile.mkstemp(suffix=suffix)[1])

    output_path.write_bytes(audio_bytes)
    return output_path
