# 🤖 Multimodal AI Assistant

A powerful AI assistant that supports both **text and voice** input/output, with integrated **web search** capabilities powered by OpenAI's GPT-4.

## ✨ Features

- 🎤 **Voice Input**: Speak to the AI using your microphone
- 🔊 **Voice Output**: AI responds with natural-sounding speech
- 💬 **Text Chat**: Traditional text-based conversation
- 🔍 **Web Search**: Automatically searches the web when needed for current information
- 🧠 **Smart Context**: Knows when to search vs. when to use its training data
- 📜 **Conversation History**: Maintains context throughout your conversation
- 🎛️ **Flexible Modes**: Switch between text and voice seamlessly

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (already configured in `.env`)
- Microphone (for voice input)
- Speakers (for voice output)

### Installation

#### Option 1: Automated Setup (Linux/macOS)

```bash
chmod +x setup.sh
./setup.sh
```

#### Option 2: Manual Setup

1. **Install system dependencies:**

   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pyaudio portaudio19-dev espeak
   ```

   **macOS:**
   ```bash
   brew install portaudio espeak
   ```

   **Windows:**
   - Download and install PyAudio from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Assistant

```bash
python3 main.py
```

## 📖 Usage Guide

### Main Menu Options

When you start the assistant, you'll see a menu with these options:

1. **Chat with text input** - Type your messages
2. **Chat with voice input** - Speak your messages
3. **Toggle auto-speak** - Turn voice responses on/off
4. **Search the web** - Perform a web search
5. **Ask question with web search** - Ask a question with web results
6. **Clear conversation history** - Start a fresh conversation
7. **Test voice output** - Test the text-to-speech
8. **Exit** - Close the application

### Example Conversations

#### Text Chat (No Web Search Needed)
```
You: Tell me a story about a robot
🤖 AI: Once upon a time, in a bustling city of the future...
```

#### Voice Chat
```
🎤 Press Enter and speak...
[You speak: "What's the weather like today?"]
✅ You said: What's the weather like today?
🔍 Searching the web...
🤖 AI: [Provides current weather information]
🔊 [AI speaks the response]
```

#### Questions That Trigger Web Search
The AI automatically searches the web when you ask about:
- Current events or news
- Today's weather
- Recent information (2023-2025)
- Stock prices
- Latest updates
- "Who is...", "What happened...", etc.

#### Questions That Don't Need Web Search
These are answered directly from the AI's knowledge:
- "Tell me a story"
- "Explain quantum physics"
- "Write a poem"
- "Help me with coding"
- "What is the capital of France?"

## 🎯 Features in Detail

### Voice Recognition
- Uses Google Speech Recognition
- Adjusts for ambient noise automatically
- Supports natural speech patterns
- Clear error messages if speech isn't recognized

### Voice Synthesis
- Natural-sounding speech using pyttsx3
- Adjustable speed and volume
- Works offline
- Multiple voice options available

### Web Search
- Integrated DuckDuckGo search
- No API key needed for search
- Extracts relevant information
- Formats results for AI processing

### AI Intelligence
- Powered by GPT-4
- Maintains conversation context
- Intelligently decides when to search
- Provides comprehensive answers

## 🔧 Configuration

### Changing OpenAI API Key

Edit the `.env` file:
```bash
OPENAI_API_KEY=your-api-key-here
```

### Adjusting Voice Settings

In `voice_output.py`, modify these values:
```python
self.engine.setProperty('rate', 175)  # Speech speed
self.engine.setProperty('volume', 0.9)  # Volume (0.0-1.0)
```

### Customizing AI Behavior

In `ai_core.py`, edit the system message to change the AI's personality and behavior.

## 📋 File Structure

```
.
├── main.py              # Main application entry point
├── ai_core.py           # OpenAI API integration
├── voice_input.py       # Speech-to-text functionality
├── voice_output.py      # Text-to-speech functionality
├── web_search.py        # Web search integration
├── requirements.txt     # Python dependencies
├── .env                 # API keys (keep secure!)
├── setup.sh            # Automated setup script
└── README.md           # This file
```

## 🐛 Troubleshooting

### No Microphone Detected
```bash
# Test your microphone
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

### PyAudio Installation Issues
**Linux:**
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
```

**macOS:**
```bash
brew install portaudio
```

**Windows:**
- Download wheel file from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
- Install: `pip install PyAudio‑0.2.11‑cp39‑cp39‑win_amd64.whl`

### Voice Output Not Working
```bash
# Linux - Install espeak
sudo apt-get install espeak

# macOS
brew install espeak
```

### API Key Issues
- Verify your OpenAI API key in `.env`
- Check you have credits on your OpenAI account
- Ensure the key has proper permissions

## 💡 Tips

1. **Speak clearly** and at a moderate pace for best voice recognition
2. **Use voice mode** for a more natural conversation experience
3. **Let the AI decide** when to search - it's smart about it!
4. **Clear history** if you want to start a new topic
5. **Test your microphone** before starting if voice input isn't working

## 🔐 Security

- **Never commit your `.env` file** to version control
- Keep your OpenAI API key secure
- The `.env` file is included in this project but should be kept private

## 📝 License

This project is provided as-is for personal and educational use.

## 🤝 Support

If you encounter any issues:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Ensure your API key is valid
4. Test your microphone and speakers

## 🎉 Enjoy!

Your multimodal AI assistant is ready to help you with information, conversations, stories, and more - all through voice or text!

---

**Made with ❤️ using OpenAI GPT-4, Python, and open-source libraries**
