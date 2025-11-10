#!/usr/bin/env python3
"""
Multimodal AI Assistant
Supports both text and voice input/output with optional web search.
"""

import sys
from ai_assistant import AIAssistant
from voice_handler import VoiceHandler
from web_search import WebSearch

class MultimodalAIAssistant:
    def __init__(self):
        """Initialize the multimodal AI assistant."""
        print("Initializing AI Assistant...")
        try:
            self.ai = AIAssistant()
            self.voice = VoiceHandler()
            self.web_search = WebSearch()
            print("AI Assistant ready!")
        except Exception as e:
            print(f"Error initializing assistant: {e}")
            sys.exit(1)
    
    def process_query(self, user_input: str, use_voice_output: bool = True, use_web_search: bool = None):
        """
        Process a user query and return response.
        
        Args:
            user_input: User's text or voice input
            use_voice_output: Whether to speak the response
            use_web_search: Whether to use web search (None = auto-detect)
        """
        if not user_input or not user_input.strip():
            return
        
        user_input = user_input.strip()
        
        # Auto-detect if web search is needed
        if use_web_search is None:
            use_web_search = self.ai._should_use_web_search(user_input)
        
        # Perform web search if needed
        web_context = None
        if use_web_search:
            print("Searching the web for current information...")
            web_context = self.web_search.search(user_input)
            if web_context:
                print("Found relevant information from the web.")
            else:
                print("No relevant web results found, using AI knowledge only.")
        
        # Get AI response
        print("Thinking...")
        response = self.ai.get_response(user_input, use_web_search=use_web_search, web_context=web_context)
        
        # Output response
        if use_voice_output:
            self.voice.speak(response)
        else:
            print(f"\nAI: {response}\n")
        
        return response
    
    def run_interactive(self):
        """Run the interactive assistant loop."""
        print("\n" + "="*60)
        print("Multimodal AI Assistant")
        print("="*60)
        print("\nCommands:")
        print("  - Type your message and press Enter for text input")
        print("  - Type 'voice' or 'v' to use voice input")
        print("  - Type 'text-only' or 't' to disable voice output")
        print("  - Type 'voice-on' or 'vo' to enable voice output")
        print("  - Type 'search' or 's' followed by your query to force web search")
        print("  - Type 'clear' or 'c' to clear conversation history")
        print("  - Type 'quit' or 'q' to exit")
        print("="*60 + "\n")
        
        use_voice_output = True
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'q', 'exit']:
                    print("Goodbye!")
                    break
                
                elif user_input.lower() in ['clear', 'c']:
                    self.ai.clear_history()
                    print("Conversation history cleared.")
                    continue
                
                elif user_input.lower() in ['voice', 'v']:
                    print("Switching to voice input mode...")
                    voice_input = self.voice.listen()
                    if voice_input:
                        self.process_query(voice_input, use_voice_output=use_voice_output)
                    continue
                
                elif user_input.lower() in ['text-only', 't']:
                    use_voice_output = False
                    print("Voice output disabled. Responses will be text-only.")
                    continue
                
                elif user_input.lower() in ['voice-on', 'vo']:
                    use_voice_output = True
                    print("Voice output enabled.")
                    continue
                
                elif user_input.lower().startswith('search ') or user_input.lower().startswith('s '):
                    # Force web search
                    query = user_input[7:] if user_input.lower().startswith('search ') else user_input[2:]
                    if query:
                        self.process_query(query, use_voice_output=use_voice_output, use_web_search=True)
                    continue
                
                # Process regular query
                self.process_query(user_input, use_voice_output=use_voice_output)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

def main():
    """Main entry point."""
    assistant = MultimodalAIAssistant()
    assistant.run_interactive()

if __name__ == "__main__":
    main()
