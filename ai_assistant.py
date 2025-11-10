"""
Multimodal AI Assistant
Supports text and voice input/output with optional web search capabilities
"""

import os
import sys
from typing import Optional, List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class WebSearch:
    """Handles web search functionality"""
    
    def __init__(self):
        try:
            from duckduckgo_search import DDGS
            self.ddgs = DDGS()
            self.available = True
        except Exception as e:
            print(f"Warning: Web search not available: {e}")
            self.available = False
    
    def search(self, query: str, max_results: int = 5) -> List[Dict[str, str]]:
        """Search the web for information"""
        if not self.available:
            return []
        
        try:
            results = []
            search_results = self.ddgs.text(query, max_results=max_results)
            for result in search_results:
                results.append({
                    'title': result.get('title', ''),
                    'snippet': result.get('body', ''),
                    'url': result.get('href', '')
                })
            return results
        except Exception as e:
            print(f"Search error: {e}")
            return []


class VoiceInput:
    """Handles voice input (speech-to-text)"""
    
    def __init__(self):
        try:
            import speech_recognition as sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            self.available = True
            # Adjust for ambient noise
            print("Adjusting for ambient noise... Please wait.")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
        except Exception as e:
            print(f"Warning: Voice input not available: {e}")
            self.available = False
    
    def listen(self) -> Optional[str]:
        """Listen for voice input and convert to text"""
        if not self.available:
            return None
        
        try:
            import speech_recognition as sr
            with self.microphone as source:
                print("Listening... Speak now!")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Could not request results: {e}")
                return None
        except sr.WaitTimeoutError:
            print("No speech detected")
            return None
        except Exception as e:
            print(f"Voice input error: {e}")
            return None


class VoiceOutput:
    """Handles voice output (text-to-speech)"""
    
    def __init__(self):
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            # Set properties
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 0.9)  # Volume level
            self.available = True
        except Exception as e:
            print(f"Warning: Voice output not available: {e}")
            self.available = False
    
    def speak(self, text: str):
        """Convert text to speech and speak it"""
        if not self.available:
            print(f"Voice output: {text}")
            return
        
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Voice output error: {e}")
            print(f"Text: {text}")


class AIAssistant:
    """Main AI Assistant class"""
    
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = OpenAI(api_key=api_key)
        self.web_search = WebSearch()
        self.voice_input = VoiceInput()
        self.voice_output = VoiceOutput()
        self.conversation_history = []
    
    def _needs_web_search(self, query: str) -> bool:
        """Determine if the query needs web search"""
        search_keywords = [
            'search', 'find', 'latest', 'current', 'recent', 'news', 
            'what is', 'who is', 'when did', 'where is', 'how to',
            'weather', 'stock', 'price', 'update', 'information about'
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in search_keywords)
    
    def _format_search_results(self, results: List[Dict[str, str]]) -> str:
        """Format search results for the AI context"""
        if not results:
            return ""
        
        formatted = "\n\nWeb Search Results:\n"
        for i, result in enumerate(results, 1):
            formatted += f"{i}. {result['title']}\n"
            formatted += f"   {result['snippet']}\n"
            formatted += f"   Source: {result['url']}\n\n"
        return formatted
    
    def process_query(self, query: str, use_voice_output: bool = False) -> str:
        """Process a query and return a response"""
        # Check if web search is needed
        search_results = []
        if self._needs_web_search(query):
            print("Searching the web for information...")
            search_results = self.web_search.search(query)
        
        # Build the context
        system_message = """You are a helpful AI assistant. You can answer questions based on your knowledge and, when provided, web search results.
        
When web search results are provided, use them to inform your answer. When no web search results are provided, answer based on your knowledge.
You can tell stories, answer questions, provide explanations, and engage in conversation naturally."""
        
        # Add search results to context if available
        context = ""
        if search_results:
            context = self._format_search_results(search_results)
        
        # Build messages
        messages = [
            {"role": "system", "content": system_message}
        ]
        
        # Add conversation history
        messages.extend(self.conversation_history[-10:])  # Keep last 10 exchanges
        
        # Add current query with context
        user_message = query
        if context:
            user_message += context
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            # Get response from OpenAI
            # Try GPT-4 first, fall back to GPT-3.5-turbo if unavailable
            try:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
            except Exception as e:
                # Fallback to GPT-3.5-turbo if GPT-4 is unavailable
                print("Note: Using GPT-3.5-turbo (GPT-4 unavailable)")
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=1000
                )
            
            assistant_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": query})
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            # Output response
            print(f"\nAI: {assistant_response}\n")
            
            # Voice output if requested
            if use_voice_output:
                self.voice_output.speak(assistant_response)
            
            return assistant_response
            
        except Exception as e:
            error_msg = f"Error processing query: {e}"
            print(error_msg)
            return error_msg
    
    def run_interactive(self):
        """Run the assistant in interactive mode"""
        print("=" * 60)
        print("Multimodal AI Assistant")
        print("=" * 60)
        print("\nCommands:")
        print("  - Type your message and press Enter for text input")
        print("  - Type 'voice' and press Enter to use voice input")
        print("  - Type 'voice on' to enable voice output")
        print("  - Type 'voice off' to disable voice output")
        print("  - Type 'quit' or 'exit' to exit")
        print("=" * 60 + "\n")
        
        use_voice_output = False
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == 'voice':
                    # Voice input mode
                    text = self.voice_input.listen()
                    if text:
                        self.process_query(text, use_voice_output=use_voice_output)
                    continue
                
                if user_input.lower() == 'voice on':
                    use_voice_output = True
                    print("Voice output enabled")
                    continue
                
                if user_input.lower() == 'voice off':
                    use_voice_output = False
                    print("Voice output disabled")
                    continue
                
                # Process text input
                self.process_query(user_input, use_voice_output=use_voice_output)
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")


def main():
    """Main entry point"""
    try:
        assistant = AIAssistant()
        assistant.run_interactive()
    except Exception as e:
        print(f"Failed to initialize AI Assistant: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
