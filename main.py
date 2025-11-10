#!/usr/bin/env python3
"""
Multimodal AI Assistant - Main Application
Supports text and voice input/output with web search capabilities
"""

import sys
import os
from ai_core import AICore
from voice_input import VoiceInput
from voice_output import VoiceOutput
from web_search import WebSearch

class MultimodalAssistant:
    def __init__(self):
        """Initialize the multimodal AI assistant"""
        print("🤖 Initializing Multimodal AI Assistant...")
        
        self.ai = AICore()
        self.voice_input = VoiceInput()
        self.voice_output = VoiceOutput()
        self.web_search = WebSearch()
        
        self.voice_mode = False
        self.auto_speak = True
        
        print("✅ AI Assistant ready!\n")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🤖 MULTIMODAL AI ASSISTANT")
        print("="*60)
        print("Commands:")
        print("  1. Chat with text input")
        print("  2. Chat with voice input")
        print("  3. Toggle auto-speak (currently: {})".format("ON" if self.auto_speak else "OFF"))
        print("  4. Search the web")
        print("  5. Ask question with web search")
        print("  6. Clear conversation history")
        print("  7. Test voice output")
        print("  8. Exit")
        print("="*60)
    
    def text_chat(self):
        """Text-based chat mode"""
        print("\n💬 Text Chat Mode (type 'back' to return to menu)")
        print("-" * 60)
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == 'back':
                break
            
            # Check if user wants web search
            needs_search = self._check_if_needs_search(user_input)
            
            if needs_search:
                print("🔍 This seems like it needs web search. Searching...")
                search_results = self.web_search.search(user_input)
                response = self.ai.chat(user_input, use_web_search=True, search_results=search_results)
            else:
                response = self.ai.chat(user_input)
            
            print(f"\n🤖 AI: {response}")
            
            if self.auto_speak:
                print("🔊 Speaking response...")
                self.voice_output.speak(response, async_mode=False)
    
    def voice_chat(self):
        """Voice-based chat mode"""
        print("\n🎤 Voice Chat Mode (say 'back' or 'exit' to return to menu)")
        print("-" * 60)
        
        while True:
            print("\n🎤 Press Enter and speak...")
            input()  # Wait for user to press Enter
            
            # Listen to voice input
            user_input = self.voice_input.listen()
            
            if user_input.startswith("ERROR:"):
                print(f"❌ {user_input}")
                continue
            
            print(f"\n✅ You said: {user_input}")
            
            if user_input.lower() in ['back', 'exit', 'quit']:
                break
            
            # Check if user wants web search
            needs_search = self._check_if_needs_search(user_input)
            
            if needs_search:
                print("🔍 Searching the web...")
                search_results = self.web_search.search(user_input)
                response = self.ai.chat(user_input, use_web_search=True, search_results=search_results)
            else:
                response = self.ai.chat(user_input)
            
            print(f"\n🤖 AI: {response}")
            
            # Always speak in voice chat mode
            print("🔊 Speaking response...")
            self.voice_output.speak(response, async_mode=False)
    
    def _check_if_needs_search(self, query):
        """
        Determine if a query needs web search
        
        Args:
            query (str): User's query
            
        Returns:
            bool: True if web search is needed
        """
        # Keywords that suggest current information is needed
        search_keywords = [
            'current', 'today', 'latest', 'recent', 'now', 'news',
            'weather', 'stock', 'price', 'what is happening',
            'who is', 'where is', 'when is', 'search for',
            'look up', 'find information', 'what happened'
        ]
        
        query_lower = query.lower()
        
        # Check for search keywords
        for keyword in search_keywords:
            if keyword in query_lower:
                return True
        
        # Check for year references suggesting recent events
        if any(year in query_lower for year in ['2024', '2025', '2023']):
            return True
        
        return False
    
    def toggle_auto_speak(self):
        """Toggle automatic speech output"""
        self.auto_speak = not self.auto_speak
        status = "enabled" if self.auto_speak else "disabled"
        print(f"\n🔊 Auto-speak {status}")
        self.voice_output.speak(f"Auto speak {status}")
    
    def web_search_mode(self):
        """Web search mode"""
        print("\n🔍 Web Search Mode")
        print("-" * 60)
        query = input("Enter search query: ").strip()
        
        if query:
            results = self.web_search.search(query)
            print(f"\n{results}")
            
            if self.auto_speak:
                # Speak a summary instead of all results
                self.voice_output.speak(f"I found search results for {query}. Please check the screen for details.")
    
    def ask_with_search(self):
        """Ask a question and use web search to answer"""
        print("\n🔍💬 Ask with Web Search")
        print("-" * 60)
        question = input("Enter your question: ").strip()
        
        if question:
            print("🔍 Searching the web...")
            search_results = self.web_search.search(question)
            
            print("\n🤖 Generating answer based on search results...")
            response = self.ai.chat(question, use_web_search=True, search_results=search_results)
            
            print(f"\n🤖 AI: {response}")
            
            if self.auto_speak:
                print("🔊 Speaking response...")
                self.voice_output.speak(response, async_mode=False)
    
    def clear_history(self):
        """Clear conversation history"""
        self.ai.clear_history()
        print("\n✅ Conversation history cleared!")
        self.voice_output.speak("Conversation history cleared")
    
    def test_voice(self):
        """Test voice output"""
        print("\n🔊 Testing Voice Output")
        print("-" * 60)
        test_text = input("Enter text to speak (or press Enter for default): ").strip()
        
        if not test_text:
            test_text = "Hello! I am your multimodal AI assistant. I can understand both text and voice, and I can respond in both formats as well."
        
        print(f"🔊 Speaking: {test_text}")
        self.voice_output.speak(test_text)
    
    def run(self):
        """Main application loop"""
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.text_chat()
            elif choice == '2':
                self.voice_chat()
            elif choice == '3':
                self.toggle_auto_speak()
            elif choice == '4':
                self.web_search_mode()
            elif choice == '5':
                self.ask_with_search()
            elif choice == '6':
                self.clear_history()
            elif choice == '7':
                self.test_voice()
            elif choice == '8':
                print("\n👋 Goodbye!")
                self.voice_output.speak("Goodbye! Have a great day!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")

def main():
    """Entry point"""
    try:
        assistant = MultimodalAssistant()
        assistant.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
