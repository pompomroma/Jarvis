# Jarvis

Jarvis is a multimodal personal assistant powered by OpenAI. The assistant can understand conversations delivered as text or spoken voice, answer with natural language, and speak its responses aloud. When a prompt requires fresh information, Jarvis can optionally pull recent facts from the web; otherwise it relies on the model's built-in knowledge so it can still tell you a story or answer creative prompts completely offline.

## Features

- Conversational text interface with persistent dialogue history.
- Voice input via your system microphone, transcribed with OpenAI Whisper.
- Spoken replies rendered with OpenAI text-to-speech.
- Optional DuckDuckGo-powered web search context for up-to-date answers.

## Quick Start

1. **Prerequisites**
   - Python ≥ 3.10.
   - Working microphone and speakers/headphones.
   - PortAudio runtime (required for `sounddevice`). On Debian/Ubuntu: `sudo apt install portaudio19-dev`.

2. **Clone & install**
   ```bash
   cd /workspace
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configuration**
   - Copy the environment template: `cp .env.example .env`.
   - Edit `.env` and set `OPENAI_API_KEY` to your project key (for example, the one you supplied: `sk-proj-UU5E…`). Never commit this file.
   - Optionally adjust the model name, default voice, or search preferences.

4. **Run the assistant**
   ```bash
   python -m src.main
   ```

## Using the CLI

- Type any message and press Enter to chat.
- Append `--web` to a message to force a contextual web search (e.g., `Latest SpaceX launch --web`).
- Enter `/voice` to record a 12-second voice prompt without web search.
- Enter `/voice web` to record a voice prompt and preface the model with web results.
- Enter `/quit` to leave the session.

After each reply Jarvis speaks the answer aloud. If audio playback fails (for example, if another program blocks the audio device) you can still read the text in the terminal and open the generated WAV file manually.

## Notes & Troubleshooting

- The first voice recording may take a couple of seconds while the microphone stream opens.
- If you see PortAudio-related errors, ensure the PortAudio libraries are installed and your user has permission to access the microphone.
- Web search uses DuckDuckGo and only shares short snippets with the model; no personal data is transmitted beyond your prompt and the generated search query.