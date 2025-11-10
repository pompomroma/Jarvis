# Multimodal AI Assistant

This project provides a Python-based personal assistant that:

- accepts commands via keyboard or microphone (speech-to-text),
- replies with written text and optionally plays synthesized speech,
- decides when to answer from its own knowledge versus performing a live web search (if a search key is configured).

## 1. Prerequisites

- Python 3.10 or newer
- `portaudio` development headers (required for `sounddevice`)
  - Ubuntu/Debian: `sudo apt install python3-dev portaudio19-dev`
- A working microphone and speakers/headphones for voice I/O

## 2. Installation

```bash
git clone <this-repo-url>
cd <repo>
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Configuration

Create a `.env` file (or export variables in your shell) with the credentials you want to use:

```
OPENAI_API_KEY=your-openai-api-key
# Optional: override defaults
# OPENAI_RESPONSES_MODEL=gpt-4o-mini
# OPENAI_TTS_VOICE=alloy
# ENABLE_TTS=true
# ENABLE_AUTO_SEARCH=true
# SEARCH_CONFIDENCE_THRESHOLD=0.6
# MAX_SEARCH_RESULTS=3
```

> ⚠️ Never commit or share your real API keys. Keep them private and scoped.

To enable web search, also provide a Tavily API key:

```
TAVILY_API_KEY=your-tavily-api-key
```

## 4. Usage

### Text-only mode

```bash
python -m src.main
```

### Voice-enabled mode

```bash
python -m src.main --voice --speak
```

- `--voice`: capture microphone input each turn and transcribe it automatically.
- `--speak`: synthesise the assistant's reply to audio and play it through your speakers.
- `--duration`: control the maximum microphone capture time (default 8 seconds).
- `--force-search`: force a web search before every reply.

Say or type `exit`/`quit` to end the session.

## 5. How It Works

- The assistant uses OpenAI's Responses API for reasoning and text generation.
- Microphone capture relies on `sounddevice`; transcription uses OpenAI's Whisper (`gpt-4o-transcribe`).
- Text-to-speech is produced with `gpt-4o-mini-tts` and played locally via `simpleaudio`.
- A lightweight local knowledge file (`knowledge/seed.txt`) helps the model respond even without searching.
- When the prompt looks time-sensitive (e.g., mentions "latest news"), the assistant attempts a Tavily web search and shares short citations with the reply.

## 6. Extending

- Add more documents to the `knowledge/` folder and point `LOCAL_MEMORY_PATH` to a custom file.
- Swap `TavilySearchClient` in `src/assistant/service.py` with another provider if you prefer a different search API.
- Build a GUI or REST wrapper around `MultimodalAssistant` to integrate it with other products.

## 7. Troubleshooting

- **Missing PortAudio**: Install platform-specific headers (`portaudio19-dev` on Debian/Ubuntu).
- **Audio playback issues**: Ensure your default output device is available; toggle `--speak` off if you only need text.
- **`OPENAI_API_KEY` missing**: Confirm your `.env` file is loaded or the environment variable is set in the current shell.
- **Search disabled**: Provide `TAVILY_API_KEY` or omit search-dependent features.

Enjoy building with the assistant!