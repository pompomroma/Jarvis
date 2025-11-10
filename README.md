# Multimodal AI Assistant

An intelligent AI assistant that supports both text and voice input/output, with optional web search capabilities. The assistant can work offline for creative tasks like storytelling, or search the web when you need current information.

## Features

- **Text Input**: Type your questions and commands
- **Voice Input**: Speak your questions using your microphone
- **Text Output**: Receive responses as text
- **Voice Output**: Hear responses spoken aloud
- **Smart Web Search**: Automatically searches the web when needed, but works offline for creative tasks
- **Conversation Memory**: Maintains context across multiple interactions

## Requirements

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/Headphones (for voice output)
- Internet connection (for API calls and optional web search)

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install system dependencies for audio:**

   **On Ubuntu/Debian:**
   ```bash
   sudo apt-get update
   sudo apt-get install portaudio19-dev python3-pyaudio
   ```

   **On macOS:**
   ```bash
   brew install portaudio
   ```

   **On Windows:**
   ```bash
   # PyAudio wheels are usually available via pip
   pip install pyaudio
   ```

3. **API Key Configuration:**
   The API key is already configured in the `.env` file. If you need to change it, edit `.env` and update the `OPENAI_API_KEY` value.

## Usage

Run the assistant:
```bash
python ai_assistant.py
```

### Commands

- **Text Input**: Simply type your message and press Enter
- **Voice Input**: Type `voice` and press Enter, then speak your question
- **Enable Voice Output**: Type `voice on` to hear responses spoken
- **Disable Voice Output**: Type `voice off` to disable voice output
- **Exit**: Type `quit`, `exit`, or `q` to exit

### Examples

**Text Interaction:**
```
You: Tell me a story about a brave knight
AI: [Responds with a story]

You: What's the weather like today?
AI: [Searches web and provides current weather information]
```

**Voice Interaction:**
```
You: voice
[Speaks into microphone]
AI: [Responds with text and optionally voice]
```

## How It Works

1. **Input Detection**: The assistant accepts both text and voice input
2. **Query Analysis**: Determines if web search is needed based on keywords
3. **Web Search** (when needed): Searches DuckDuckGo for current information
4. **AI Processing**: Uses OpenAI GPT-4 to generate intelligent responses
5. **Output**: Displays text response and optionally speaks it aloud

## Features Explained

### Smart Web Search
The assistant automatically detects when you need current information (e.g., "what's the weather", "latest news") and searches the web. For creative tasks like storytelling or general questions, it uses its built-in knowledge without searching.

### Voice Input
Uses Google's Speech Recognition API to convert your speech to text. Make sure your microphone is working and there's minimal background noise.

### Voice Output
Uses pyttsx3 for text-to-speech. The voice output can be toggled on/off during the session.

## Troubleshooting

**Voice input not working:**
- Check microphone permissions
- Ensure PyAudio is installed correctly
- Try adjusting microphone volume
- Check for background noise

**Web search not working:**
- Check your internet connection
- DuckDuckGo search may be rate-limited; wait a moment and try again

**API errors:**
- Verify your OpenAI API key is correct
- Check your API usage limits
- Ensure you have internet connectivity

## Notes

- The assistant maintains conversation history for context
- Web search is automatic and only used when needed
- Voice features require proper audio hardware setup
- The API key is stored in `.env` file - keep it secure