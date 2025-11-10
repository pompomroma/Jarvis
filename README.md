# Multimodal AI Assistant

A sophisticated AI assistant that supports both text and voice input/output, with intelligent web search capabilities when needed.

## Features

- **Text Input**: Type your questions and commands
- **Voice Input**: Speak your questions using speech recognition
- **Text Output**: Display responses in the terminal
- **Voice Output**: Hear responses via text-to-speech
- **Smart Web Search**: Automatically detects when web search is needed, but can work offline for creative tasks like storytelling
- **Manual Web Search**: Force web search for specific queries
- **Conversation Memory**: Maintains context across multiple interactions

## Requirements

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/Headphones (for voice output)
- Internet connection (for OpenAI API and optional web search)

## Installation

1. **Install system dependencies** (Linux):

```bash
# For Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-pyaudio portaudio19-dev espeak espeak-data libespeak1 libespeak-dev

# For Fedora/CentOS
sudo yum install python3-pyaudio portaudio-devel espeak espeak-devel
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

## Configuration

The API key is already configured in the `.env` file. If you need to change it, edit `.env`:

```
OPENAI_API_KEY=your-api-key-here
```

## Usage

Run the assistant:

```bash
python main.py
```

### Commands

Once the assistant is running, you can use the following commands:

- **Type your message**: Just type and press Enter for text input
- **`voice` or `v`**: Switch to voice input mode (speak your question)
- **`text-only` or `t`**: Disable voice output (text responses only)
- **`voice-on` or `vo`**: Enable voice output
- **`search <query>` or `s <query>`**: Force web search for a specific query
- **`clear` or `c`**: Clear conversation history
- **`quit` or `q`**: Exit the assistant

### Examples

**Text Input:**
```
You: What is the capital of France?
AI: [speaks and displays] The capital of France is Paris.
```

**Voice Input:**
```
You: voice
Listening... (speak now)
You said: Tell me a story about a brave knight
AI: [speaks and displays] Once upon a time, in a kingdom far away...
```

**Web Search:**
```
You: What's the weather like today?
[Automatically searches web and provides current weather]
```

**Creative Content (No Web Search):**
```
You: Tell me a joke
AI: [Uses AI knowledge, no web search needed]
```

## How It Works

1. **Input Detection**: The assistant accepts both text and voice input
2. **Smart Search Detection**: Automatically determines if web search is needed based on query keywords
3. **Response Generation**: Uses OpenAI GPT-4 to generate intelligent responses
4. **Output**: Provides both text and voice output simultaneously

## Troubleshooting

### Microphone Issues
- Ensure your microphone is connected and working
- Check system microphone permissions
- Try adjusting microphone volume in system settings

### Audio Output Issues
- Ensure speakers/headphones are connected
- Check system audio settings
- On Linux, you may need to install additional audio drivers

### API Errors
- Verify your OpenAI API key is correct
- Check your internet connection
- Ensure you have API credits available

### Import Errors
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- For PyAudio issues on Linux, install system dependencies first (see Installation)

## Project Structure

```
.
├── main.py              # Main application entry point
├── ai_assistant.py      # OpenAI integration and conversation handling
├── voice_handler.py     # Speech-to-text and text-to-speech
├── web_search.py       # Web search functionality
├── requirements.txt     # Python dependencies
├── .env                # API key configuration
└── README.md           # This file
```

## Notes

- The assistant uses Google's speech recognition (free, no API key needed)
- Text-to-speech uses pyttsx3 (offline, no internet required for TTS)
- Web search uses DuckDuckGo (privacy-focused, no API key needed)
- Conversation history is maintained in memory (cleared on restart)

## License

This project is provided as-is for educational and personal use.
