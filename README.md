# 🤖 Multimodal AI Assistant

A sophisticated AI assistant powered by OpenAI's GPT-4 that can understand and respond through both **text** and **voice**. It features intelligent web search capabilities and can engage in conversations, tell stories, answer questions, and much more!

## ✨ Features

- 📝 **Text Input/Output**: Traditional text-based interaction
- 🎤 **Voice Input**: Speak your commands naturally using speech recognition
- 🔊 **Voice Output**: Hear responses with text-to-speech
- 🌐 **Web Search**: Automatic web searching for current information when needed
- 🧠 **Smart Decision Making**: AI decides when to search the web vs. use its own knowledge
- 💬 **Conversation History**: Maintains context throughout your conversation
- 🎯 **Multi-mode Support**: Switch between text and voice modes seamlessly

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Microphone (for voice input)
- Speakers/headphones (for voice output)
- Internet connection (for API calls and web search)

### Installation

1. **Clone or download this repository**

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

**Note for Linux users**: You may need to install additional audio dependencies:
```bash
# For Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-pyaudio
sudo apt-get install espeak ffmpeg libespeak1

# For Fedora
sudo dnf install portaudio-devel
sudo dnf install espeak ffmpeg
```

**Note for macOS users**: PyAudio installation:
```bash
brew install portaudio
pip install pyaudio
```

3. **Set up your API key**:

The OpenAI API key is already configured in the `.env` file. If you need to change it, edit the `.env` file:

```bash
OPENAI_API_KEY=your_api_key_here
```

### Running the Assistant

**Basic usage (text mode with voice output)**:
```bash
python main.py
```

**Start in voice input mode**:
```bash
python main.py --voice
```

**Text only (no voice output)**:
```bash
python main.py --no-voice-output
```

**Use Google TTS for better voice quality** (requires internet):
```bash
python main.py --gtts
```

**View all options**:
```bash
python main.py --help
```

## 📖 Usage Guide

### Text Mode

1. Type your message and press Enter
2. The AI will respond in text (and voice if enabled)
3. Special commands:
   - `quit` or `exit` - Close the assistant
   - `voice` - Switch to voice input mode
   - `clear` - Clear conversation history

### Voice Mode

1. Wait for the "Ready to listen..." prompt
2. Speak your command clearly
3. The AI will process and respond
4. Special voice commands:
   - Say "quit" or "exit" to close
   - Say "text mode" to switch to text input
   - Say "clear history" to reset conversation

## 💡 Example Interactions

### Creative Tasks (No Web Search)
```
You: Tell me a story about a space explorer
AI: [Generates creative story using its knowledge]
```

### Current Information (With Web Search)
```
You: What's the latest news about AI?
AI: [Searches web and provides current information]
```

### General Conversation
```
You: How can I improve my productivity?
AI: [Provides helpful advice based on its knowledge]
```

### Weather and Current Events
```
You: What's the weather today?
AI: [Searches for current weather information]
```

## 🏗️ Project Structure

```
/workspace/
├── main.py              # Main application entry point
├── ai_assistant.py      # OpenAI API integration
├── voice_input.py       # Speech-to-text module
├── voice_output.py      # Text-to-speech module
├── web_search.py        # Web search functionality
├── requirements.txt     # Python dependencies
├── .env                 # API key configuration
└── README.md           # This file
```

## 🔧 Configuration

### Voice Settings

Edit `voice_output.py` to customize:
- Voice selection (male/female)
- Speech rate
- Volume

### AI Behavior

Edit `ai_assistant.py` to customize:
- Model selection (currently using `gpt-4o-mini`)
- Response length
- Temperature (creativity level)
- Search triggers

## 🌐 Web Search

The assistant intelligently determines when to search the web based on your query. It will search for:

- Current events and news
- Weather information
- Latest prices or statistics
- Specific factual queries
- Anything with keywords like "current", "latest", "today", etc.

It will NOT search for:
- Creative requests (stories, writing, etc.)
- General knowledge questions
- Conversational topics

## 🎯 Features Breakdown

### 1. Speech Recognition
- Uses Google's speech recognition service
- Automatic ambient noise adjustment
- Retry mechanism for failed recognition
- Support for multiple languages

### 2. Text-to-Speech
- **pyttsx3** (default): Offline, fast, cross-platform
- **gTTS** (optional): Online, better quality, more natural

### 3. AI Intelligence
- Powered by OpenAI's GPT-4o-mini
- Context-aware conversations
- Intelligent web search decisions
- Maintains conversation history

### 4. Web Search
- DuckDuckGo search integration (privacy-friendly)
- Regular web search
- News search
- No tracking or ads

## 🐛 Troubleshooting

### Microphone Issues
- Check microphone permissions in your system settings
- Test microphone with other applications
- Try increasing the timeout: Edit `voice_input.py`

### Voice Output Issues
- **Linux**: Install espeak and ffmpeg
- **macOS**: Built-in speech synthesis should work
- **Windows**: Should work out of the box
- Try using `--gtts` flag for Google TTS

### API Errors
- Verify your OpenAI API key in `.env`
- Check your internet connection
- Ensure you have API credits

### Installation Issues
- Make sure you have Python 3.8+
- Install audio dependencies for your OS
- Try creating a virtual environment:
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

## 📝 Advanced Usage

### Using as a Library

You can import and use the assistant in your own Python scripts:

```python
from ai_assistant import AIAssistant
from web_search import WebSearch

ai = AIAssistant()
search = WebSearch()

# Generate a response
response = ai.generate_response("Tell me a joke")
print(response)

# Search the web
results = search.search("latest AI news")
print(results)
```

## 🔒 Security Notes

- Your API key is stored in `.env` - keep this file secure
- Don't commit `.env` to version control
- The assistant uses OpenAI's API - data is sent to their servers
- Web searches use DuckDuckGo for privacy

## 🆘 Support

If you encounter issues:
1. Check the Troubleshooting section above
2. Verify all dependencies are installed correctly
3. Check your API key is valid
4. Ensure your internet connection is stable

## 🎉 Enjoy!

You now have a powerful multimodal AI assistant that can understand and respond through text and voice, with intelligent web search capabilities. Have fun exploring its capabilities!