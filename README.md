# Multimodal Voice & Text AI Assistant

This project provides a Python assistant that can understand both text and spoken commands, respond with natural language, and speak its answers aloud. It can operate fully offline from the web (using the model's own knowledge), or optionally augment its answers with live web search results when you prefix your request with `search:`.

## Features
- Conversational AI powered by OpenAI `gpt-4o-mini`
- Speech-to-text transcription via `gpt-4o-mini-transcribe`
- Text-to-speech playback using `gpt-4o-mini-tts`
- Optional DuckDuckGo web search integration (`search: your query`)
- Conversation history to keep context across turns
- Configurable settings in `AssistantConfig`

## Prerequisites
- Python 3.10 or newer
- OpenAI API access (set `OPENAI_API_KEY`)
- Audio hardware (microphone + speakers/headphones)
- On Linux, ensure PortAudio is installed (e.g. `sudo apt install portaudio19-dev`)

## Setup
1. Clone this repo and change into the project directory.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure your OpenAI API key:
   ```bash
   cp .env.example .env
   # edit .env and replace with your actual key
   ```
   Alternatively, export `OPENAI_API_KEY` directly in your shell.

## Running the Assistant
```bash
python src/assistant.py
```

At the prompt:
- Enter `t` to type a message.
- Enter `v` to speak a request (press Enter to finish recording).
- Enter `q` to quit.

To force a web-powered answer, prefix your request with `search:` (e.g. `search: latest Mars rover news`). Otherwise, the assistant answers from its built-in reasoning.

## Notes
- Recorded audio snippets are stored temporarily in `./temp` and deleted after processing.
- Customize behaviour (models, temperatures, timeouts, audio playback) by adjusting `AssistantConfig` in `src/assistant.py`.
- For better voice detection you can increase `max_record_seconds` or `minimum_voice_seconds` in the config.
