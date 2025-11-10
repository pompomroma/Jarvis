#!/usr/bin/env python3
"""
Multimodal AI Assistant
Supports text and voice input/output with web search capability
"""

import os
import sys
import json
import re
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

import openai
import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

class MultimodalAIAssistant:
    def __init__(self, api_key: str):
        """Initialize the AI Assistant with OpenAI API key"""
        self.api_key = api_key
        openai.api_key = api_key
        self.client = openai.OpenAI(api_key=api_key)
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Conversation history
        self.conversation_history: List[dict] = []
        
        # Keywords that suggest web search is needed
        self.search_keywords = [
            'current', 'latest', 'recent', 'today', 'now', 'what is', 'who is',
            'when did', 'where is', 'how to', 'news', 'weather', 'price', 'stock',
            'search', 'find', 'look up', 'information about'
        ]
        
        print("🤖 AI Assistant initialized successfully!")
        print("📝 You can interact via text or voice")
        print("💬 Type 'voice' to switch to voice mode, 'text' for text mode")
        print("🔍 The assistant will automatically search the web when needed")
        print("Type 'quit' or 'exit' to stop\n")

    def needs_web_search(self, query: str) -> bool:
        """Determine if the query requires web search"""
        query_lower = query.lower()
        
        # Check for explicit search requests
        if any(keyword in query_lower for keyword in ['search', 'look up', 'find information']):
            return True
        
        # Check for time-sensitive queries
        if any(keyword in query_lower for keyword in ['current', 'latest', 'recent', 'today', 'now', 'news']):
            return True
        
        # Check for factual queries that might need current data
        if query_lower.startswith(('what is', 'who is', 'when did', 'where is')):
            # But not for general knowledge questions that don't need current info
            if any(word in query_lower for word in ['story', 'tell me a', 'explain', 'describe']):
                return False
            return True
        
        return False

    def search_web(self, query: str, max_results: int = 3) -> str:
        """Search the web for information"""
        try:
            print(f"🔍 Searching the web for: {query}")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                
            if not results:
                return "No search results found."
            
            # Format search results
            search_info = "Here's what I found:\n\n"
            for i, result in enumerate(results, 1):
                search_info += f"{i}. {result.get('title', 'No title')}\n"
                search_info += f"   {result.get('body', 'No description')[:200]}...\n"
                search_info += f"   Source: {result.get('href', 'Unknown')}\n\n"
            
            return search_info
        except Exception as e:
            print(f"⚠️ Web search error: {e}")
            return f"Unable to search the web: {str(e)}"

    def get_ai_response(self, user_input: str, use_web_search: bool = False) -> str:
        """Get response from OpenAI API"""
        try:
            # Add web search context if needed
            system_message = """You are a helpful AI assistant. You can answer questions, tell stories, 
            have conversations, and provide information. Be conversational, friendly, and helpful."""
            
            if use_web_search:
                search_results = self.search_web(user_input)
                system_message += f"\n\nHere is some web search information that might be relevant:\n{search_results}"
            
            # Prepare messages
            messages = [
                {"role": "system", "content": system_message}
            ]
            
            # Add conversation history (last 10 exchanges)
            messages.extend(self.conversation_history[-10:])
            
            # Add current user message
            messages.append({"role": "user", "content": user_input})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
            
        except Exception as e:
            return f"Error getting AI response: {str(e)}"

    def listen_for_voice(self) -> Optional[str]:
        """Listen for voice input and convert to text"""
        try:
            print("🎤 Listening... Speak now!")
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("🔄 Processing voice input...")
            # Recognize speech using Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            print(f"📝 You said: {text}")
            return text
            
        except sr.WaitTimeoutError:
            print("⏱️ No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"❌ Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"❌ Error listening: {e}")
            return None

    def speak(self, text: str):
        """Convert text to speech"""
        try:
            print(f"🔊 Speaking: {text[:100]}...")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"⚠️ Error with text-to-speech: {e}")

    def process_input(self, user_input: str, voice_mode: bool = False):
        """Process user input and generate response"""
        if not user_input or user_input.strip() == "":
            return
        
        user_input = user_input.strip()
        
        # Determine if web search is needed
        use_web_search = self.needs_web_search(user_input)
        
        # Get AI response
        response = self.get_ai_response(user_input, use_web_search=use_web_search)
        
        # Display text response
        print(f"\n🤖 Assistant: {response}\n")
        
        # Speak response if in voice mode
        if voice_mode:
            self.speak(response)

    def run_text_mode(self):
        """Run the assistant in text mode"""
        print("\n📝 Text mode activated. Type your messages below.\n")
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'voice':
                    self.run_voice_mode()
                    break
                elif user_input:
                    self.process_input(user_input, voice_mode=False)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break

    def run_voice_mode(self):
        """Run the assistant in voice mode"""
        print("\n🎤 Voice mode activated. Say 'exit' or 'quit' to stop.\n")
        while True:
            try:
                user_input = self.listen_for_voice()
                
                if user_input:
                    user_input_lower = user_input.lower()
                    if user_input_lower in ['quit', 'exit', 'stop']:
                        print("👋 Goodbye!")
                        self.speak("Goodbye!")
                        break
                    elif user_input_lower == 'text mode':
                        print("Switching to text mode...")
                        self.run_text_mode()
                        break
                    else:
                        self.process_input(user_input, voice_mode=True)
                        
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break

    def run(self):
        """Main run loop"""
        print("\n" + "="*60)
        print("🤖 Multimodal AI Assistant")
        print("="*60)
        
        while True:
            try:
                mode = input("\nChoose mode - 'text' or 'voice' (default: text): ").strip().lower()
                
                if mode == 'voice' or mode == 'v':
                    self.run_voice_mode()
                    break
                elif mode == 'text' or mode == 't' or mode == '':
                    self.run_text_mode()
                    break
                elif mode in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter 'text' or 'voice'.")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break


def main():
    """Main entry point"""
    # Get API key from environment or use provided one
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please set it in .env file or environment variables.")
        sys.exit(1)
    
    # Initialize and run the assistant
    assistant = MultimodalAIAssistant(api_key)
    assistant.run()


if __name__ == "__main__":
    main()
