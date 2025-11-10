# Multimodal AI Assistant

This project provides a Python-based assistant that can:

- chat through text and, when available, microphone input;
- reply with spoken audio as well as text;
- fall back to its built-in reasoning for creative requests (e.g., storytelling);
- optionally pull in fresh information via DuckDuckGo search snippets when prompted.

## Prerequisites

- Python 3.10+
- PortAudio runtime (`libportaudio2` on Debian/Ubuntu) for microphone and speaker access
- A valid OpenAI API key with access to GPT-4o mini, speech, and transcription models

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Copy the environment template and add your actual key (never commit real keys):
   ```bash
   cp .env.example .env
   # edit .env to set OPENAI_API_KEY=sk-...
   ```

## Usage

- Text-only chat:
  ```bash
  python main.py --mode text
  ```
- Voice-enabled chat (requires working microphone and speakers):
  ```bash
  python main.py --mode voice
  ```

### Voice Mode Notes

- Press Enter to begin recording; the assistant captures up to `MAX_VOICE_RECORD_SECONDS`.
- After the response plays, the session loops for the next interaction.
- If audio devices are missing, the assistant falls back to text-only operation.

### Web Search

- The assistant automatically attempts web search for queries containing phrases like “search”, “look up”, or “latest”.
- Prefix a prompt with `search:` to force lookup, or include `no-search` to keep the response offline.

## Security

- Keep your `.env` out of version control.
- Rotate API keys if you suspect exposure.
- Review logs/output before sharing to avoid leaking secrets.