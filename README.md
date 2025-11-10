# Multimodal AI Assistant

An intelligent AI assistant that supports both text and voice interactions, with automatic web search capabilities when needed.

## Features

- 🎤 **Voice Input**: Speak your commands using speech recognition
- 🔊 **Voice Output**: Hear responses via text-to-speech
- 📝 **Text Input/Output**: Traditional text-based interaction
- 🔍 **Smart Web Search**: Automatically searches the web when current information is needed
- 🧠 **Offline Capability**: Works without web search for general questions, stories, and conversations
- 💬 **Conversation Memory**: Maintains context throughout the conversation

## Requirements

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/Headphones (for voice output)
- Internet connection (for AI API and optional web search)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. For Linux users, you may need to install additional system dependencies:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# Fedora
sudo dnf install portaudio-devel python3-pyaudio
```

3. The API key is already configured in the `.env` file.

## Usage

Run the assistant:
```bash
python assistant.py
```

### Modes

1. **Text Mode**: Type your questions and receive text responses
   - Type `voice` to switch to voice mode
   - Type `quit` or `exit` to stop

2. **Voice Mode**: Speak your questions and receive voice responses
   - Say `text mode` to switch to text mode
   - Say `exit` or `quit` to stop

### Examples

**Text Mode:**
```
You: Tell me a story about a brave knight
🤖 Assistant: [Tells a story without web search]

You: What's the current weather in New York?
🤖 Assistant: [Searches web and provides current information]
```

**Voice Mode:**
- Speak naturally: "What is artificial intelligence?"
- The assistant will listen, process, and respond both in text and voice

## How It Works

- **Web Search Detection**: The assistant automatically detects when a query needs current information (e.g., "current weather", "latest news") and performs a web search
- **Offline Mode**: For general questions, stories, explanations, and conversations, it works directly with the AI model without web search
- **Smart Context**: Maintains conversation history for better context understanding

## Configuration

The API key is stored in `.env` file. You can modify it if needed:
```
OPENAI_API_KEY=your_api_key_here
```

## Troubleshooting

- **Microphone not working**: Check your system audio settings and ensure the microphone is enabled
- **Speech recognition errors**: Ensure you have an internet connection (uses Google Speech Recognition)
- **Audio output issues**: Check your system volume and audio output settings
- **Web search fails**: The assistant will still respond using its knowledge base

## Notes

- Voice recognition uses Google Speech Recognition API (requires internet)
- Text-to-speech uses offline pyttsx3 engine (works without internet)
- Web search uses DuckDuckGo search (no API key required)
- AI responses use OpenAI GPT-4 model