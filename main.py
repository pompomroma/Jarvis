#!/usr/bin/env python3
"""
Multimodal AI Assistant
Main application that integrates text/voice input and output with AI responses
"""

import sys
import time
from ai_assistant import AIAssistant
from voice_input import VoiceInput
from voice_output import VoiceOutput
from web_search import WebSearch

class MultimodalAssistant:
    def __init__(self, use_voice_output=True, use_gtts=False):
        """
        Initialize the multimodal AI assistant
        
        Args:
            use_voice_output: Enable voice output
            use_gtts: Use Google TTS instead of pyttsx3
        """
        print("🤖 Initializing Multimodal AI Assistant...")
        
        try:
            self.ai = AIAssistant()
            self.voice_input = VoiceInput()
            self.voice_output = VoiceOutput(use_gtts=use_gtts) if use_voice_output else None
            self.web_search = WebSearch()
            self.use_voice_output = use_voice_output
            
            print("✅ AI Assistant initialized successfully!")
            
        except Exception as e:
            print(f"❌ Error initializing assistant: {e}")
            sys.exit(1)
    
    def process_input(self, user_input, input_mode="text"):
        """
        Process user input and generate response
        
        Args:
            user_input: The user's input text
            input_mode: "text" or "voice"
        
        Returns:
            AI response text
        """
        if not user_input or not user_input.strip():
            return None
        
        print(f"\n{'='*60}")
        print(f"📥 Input ({input_mode}): {user_input}")
        print(f"{'='*60}")
        
        # Check if web search is needed
        needs_search = self.ai.should_search_web(user_input)
        web_context = None
        
        if needs_search:
            print("🌐 Web search required, fetching information...")
            # Check for news-related queries
            if any(word in user_input.lower() for word in ['news', 'latest', 'recent']):
                web_context = self.web_search.search_news(user_input)
            else:
                web_context = self.web_search.search(user_input)
            print("✅ Web search completed\n")
        
        # Generate AI response
        print("🧠 Generating AI response...")
        response = self.ai.generate_response(user_input, web_context)
        
        print(f"\n💬 AI Response: {response}")
        print(f"{'='*60}\n")
        
        # Speak the response if voice output is enabled
        if self.use_voice_output and self.voice_output:
            self.voice_output.speak(response)
        
        return response
    
    def text_mode(self):
        """Run in text-only mode"""
        print("\n" + "="*60)
        print("📝 TEXT MODE")
        print("="*60)
        print("Type your messages and press Enter.")
        print("Commands:")
        print("  'quit' or 'exit' - Exit the assistant")
        print("  'voice' - Switch to voice mode")
        print("  'clear' - Clear conversation history")
        print("="*60 + "\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                    print("👋 Goodbye!")
                    if self.use_voice_output and self.voice_output:
                        self.voice_output.speak("Goodbye!")
                    break
                
                if user_input.lower() == 'voice':
                    self.voice_mode()
                    continue
                
                if user_input.lower() == 'clear':
                    self.ai.reset_conversation()
                    print("🗑️  Conversation history cleared.")
                    continue
                
                # Process the input
                self.process_input(user_input, input_mode="text")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def voice_mode(self):
        """Run in voice input mode"""
        print("\n" + "="*60)
        print("🎤 VOICE MODE")
        print("="*60)
        print("Speak your commands. Say 'text mode' to switch to text.")
        print("Say 'quit' or 'exit' to close the assistant.")
        print("="*60 + "\n")
        
        while True:
            try:
                print("\n👂 Ready to listen...")
                user_input = self.voice_input.listen()
                
                if not user_input:
                    continue
                
                # Check for commands
                user_input_lower = user_input.lower()
                
                if any(word in user_input_lower for word in ['quit', 'exit', 'goodbye', 'bye']):
                    print("👋 Goodbye!")
                    if self.use_voice_output and self.voice_output:
                        self.voice_output.speak("Goodbye!")
                    return
                
                if 'text mode' in user_input_lower:
                    print("Switching to text mode...")
                    return
                
                if 'clear' in user_input_lower and 'history' in user_input_lower:
                    self.ai.reset_conversation()
                    response = "Conversation history cleared."
                    print(f"💬 {response}")
                    if self.use_voice_output and self.voice_output:
                        self.voice_output.speak(response)
                    continue
                
                # Process the voice input
                self.process_input(user_input, input_mode="voice")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                return
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def run(self, mode="text"):
        """
        Run the assistant
        
        Args:
            mode: "text" or "voice" - starting mode
        """
        print("\n" + "="*60)
        print("🤖 MULTIMODAL AI ASSISTANT")
        print("="*60)
        print("Welcome! I can understand and respond in both text and voice.")
        print("I can help you with:")
        print("  • General conversations and questions")
        print("  • Telling stories and creative tasks")
        print("  • Searching the web for current information")
        print("  • And much more!")
        print("="*60)
        
        if mode == "voice":
            self.voice_mode()
        else:
            self.text_mode()


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         🤖 MULTIMODAL AI ASSISTANT 🤖                   ║
    ║                                                          ║
    ║  A sophisticated AI with text & voice capabilities      ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Parse command line arguments
    mode = "text"
    use_voice_output = True
    use_gtts = False
    
    if len(sys.argv) > 1:
        if "--voice" in sys.argv or "-v" in sys.argv:
            mode = "voice"
        if "--no-voice-output" in sys.argv:
            use_voice_output = False
        if "--gtts" in sys.argv:
            use_gtts = True
        if "--help" in sys.argv or "-h" in sys.argv:
            print("""
Usage: python main.py [OPTIONS]

Options:
  -v, --voice              Start in voice input mode
  --no-voice-output        Disable voice output (text only)
  --gtts                   Use Google TTS (requires internet, better quality)
  -h, --help               Show this help message

Examples:
  python main.py                    # Start in text mode with voice output
  python main.py --voice            # Start in voice mode
  python main.py --no-voice-output  # Text only, no speech
  python main.py --gtts             # Use Google TTS for better voice quality
            """)
            return
    
    try:
        assistant = MultimodalAssistant(
            use_voice_output=use_voice_output,
            use_gtts=use_gtts
        )
        assistant.run(mode=mode)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
