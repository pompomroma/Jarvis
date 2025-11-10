# Multimodal AI Assistant

A sophisticated AI assistant that can interact via both text and voice, with intelligent web search capabilities when needed.

## Features

- **Text Input**: Type your questions and commands
- **Voice Input**: Speak your questions using your microphone
- **Text Output**: Receive responses as text
- **Voice Output**: Hear responses spoken aloud
- **Smart Web Search**: Automatically searches the web when needed (e.g., current events, real-time data)
- **Offline Mode**: Works without web search for general questions, stories, and creative tasks

## Setup

### Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/headphones (for voice output)
- Internet connection (for API calls and optional web search)

### Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. The API key is already configured in the `.env` file.

3. For Linux users, you may need to install additional system dependencies for audio:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio

# Fedora
sudo dnf install portaudio-devel python3-pyaudio
```

## Usage

Run the assistant:
```bash
python ai_assistant.py
```

### Commands

- **Text Input**: Simply type your message and press Enter
- **Voice Input**: Type `voice` or `v` and press Enter, then speak your question
- **Text-Only Mode**: Type `text-only` or `t` to disable voice output
- **Voice Output**: Type `voice-on` or `vo` to enable voice output
- **Exit**: Type `quit`, `exit`, or `q` to exit

### Examples

**Text Input:**
```
You: Tell me a story about a robot
AI: [Responds with a story, no web search needed]
```

**Voice Input:**
```
You: voice
Listening... (speak now)
You said: What's the weather like today?
Searching the web for information...
AI: [Searches web and responds with current weather]
```

**Web Search Examples:**
- "What's the latest news about AI?"
- "Search for the current price of Bitcoin"
- "What happened today in technology?"

**Offline Examples (No Web Search):**
- "Tell me a story"
- "Explain quantum physics"
- "Write a poem about nature"
- "What is the capital of France?"

## How It Works

1. **Input Detection**: The assistant accepts both text and voice input
2. **Smart Search Detection**: Analyzes the query to determine if web search is needed
3. **Web Search (when needed)**: Uses DuckDuckGo to search for current information
4. **AI Processing**: Uses OpenAI GPT-4 to generate intelligent responses
5. **Output**: Provides responses in both text and voice formats

## Configuration

You can modify the following in `ai_assistant.py`:

- **Model**: Change `self.model` to use different OpenAI models (default: "gpt-4")
- **Speech Rate**: Adjust `self.tts_engine.setProperty('rate', 150)` for faster/slower speech
- **Volume**: Adjust `self.tts_engine.setProperty('volume', 0.9)` for louder/quieter output
- **Search Keywords**: Modify `self.search_keywords` to change when web search is triggered

## Troubleshooting

**Microphone not working:**
- Check microphone permissions
- Ensure microphone is connected and working
- Try adjusting microphone volume in system settings

**Voice recognition issues:**
- Speak clearly and at a moderate pace
- Reduce background noise
- Check internet connection (Google Speech Recognition requires internet)

**Text-to-speech not working:**
- On Linux, ensure you have espeak installed: `sudo apt-get install espeak`
- On Windows/Mac, pyttsx3 should work out of the box

**API errors:**
- Verify your API key is correct in `.env`
- Check your OpenAI account has sufficient credits
- Ensure you have internet connectivity

## License

This project is provided as-is for educational and personal use.
