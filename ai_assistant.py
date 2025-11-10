import os
import speech_recognition as sr
import pyttsx3
import openai
from dotenv import load_dotenv
from duckduckgo_search import DDGS
import re

# Load environment variables
load_dotenv()

class MultimodalAIAssistant:
    def __init__(self):
        # Initialize OpenAI client
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        self.client = openai.OpenAI(api_key=self.api_key)
        self.model = "gpt-4"
        
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Speed of speech
        self.tts_engine.setProperty('volume', 0.9)  # Volume level
        
        # Conversation history
        self.conversation_history = []
        
        # Keywords that suggest web search is needed
        self.search_keywords = [
            "search", "find", "look up", "what is", "who is", "when did",
            "where is", "latest", "recent", "current", "news", "weather",
            "price", "compare", "how to", "tutorial", "definition"
        ]
    
    def needs_web_search(self, query):
        """Determine if the query requires web search"""
        query_lower = query.lower()
        
        # Check for explicit search requests
        if any(keyword in query_lower for keyword in self.search_keywords):
            return True
        
        # Check for questions about current events, real-time data, etc.
        time_sensitive_keywords = ["today", "now", "current", "latest", "recent", "2024", "2025"]
        if any(keyword in query_lower for keyword in time_sensitive_keywords):
            return True
        
        return False
    
    def search_web(self, query, max_results=5):
        """Search the web using DuckDuckGo"""
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=max_results))
                if results:
                    # Format results for the AI
                    search_context = "\n\nWeb Search Results:\n"
                    for i, result in enumerate(results, 1):
                        search_context += f"{i}. {result.get('title', 'No title')}\n"
                        search_context += f"   {result.get('body', 'No description')}\n"
                        search_context += f"   URL: {result.get('href', 'No URL')}\n\n"
                    return search_context
                return "\n\nNo web search results found.\n"
        except Exception as e:
            print(f"Error during web search: {e}")
            return "\n\nWeb search encountered an error.\n"
    
    def get_ai_response(self, user_input, use_web_search=False):
        """Get response from OpenAI API"""
        # Add web search context if needed
        system_message = "You are a helpful AI assistant. Provide accurate and helpful responses."
        if use_web_search:
            search_results = self.search_web(user_input)
            system_message += f"\n\n{search_results}\n\nUse the web search results above to inform your response when relevant."
        else:
            system_message += " You can answer questions using your knowledge without needing to search the web."
        
        # Prepare messages
        messages = [{"role": "system", "content": system_message}]
        
        # Add conversation history
        messages.extend(self.conversation_history[-10:])  # Keep last 10 exchanges
        
        # Add current user message
        messages.append({"role": "user", "content": user_input})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            ai_response = response.choices[0].message.content
            
            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            return ai_response
        except Exception as e:
            return f"Error getting AI response: {str(e)}"
    
    def listen_to_voice(self):
        """Listen to voice input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening... (speak now)")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            print("Processing speech...")
            # Recognize speech using Google's speech recognition
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio. Please try again.")
            return None
        except sr.RequestError as e:
            print(f"Error with speech recognition service: {e}")
            return None
        except Exception as e:
            print(f"Error listening to voice: {e}")
            return None
    
    def speak(self, text):
        """Convert text to speech"""
        try:
            print(f"AI: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {e}")
            print(f"AI (text only): {text}")
    
    def process_text_input(self, text_input, voice_output=True):
        """Process text input and return response"""
        if not text_input.strip():
            return None
        
        # Determine if web search is needed
        use_web_search = self.needs_web_search(text_input)
        
        if use_web_search:
            print("Searching the web for information...")
        
        # Get AI response
        response = self.get_ai_response(text_input, use_web_search=use_web_search)
        
        # Output response
        if voice_output:
            self.speak(response)
        else:
            print(f"AI: {response}")
        
        return response
    
    def process_voice_input(self, voice_output=True):
        """Process voice input and return response"""
        # Listen to voice
        text_input = self.listen_to_voice()
        
        if text_input is None:
            return None
        
        # Process the text input
        return self.process_text_input(text_input, voice_output=voice_output)
    
    def run_interactive_mode(self):
        """Run the assistant in interactive mode"""
        print("=" * 60)
        print("Multimodal AI Assistant")
        print("=" * 60)
        print("\nCommands:")
        print("  - Type your message and press Enter for text input")
        print("  - Type 'voice' or 'v' and press Enter for voice input")
        print("  - Type 'text-only' or 't' to disable voice output")
        print("  - Type 'voice-on' or 'vo' to enable voice output")
        print("  - Type 'quit', 'exit', or 'q' to exit")
        print("=" * 60)
        
        voice_output_enabled = True
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Handle special commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                elif user_input.lower() in ['voice', 'v']:
                    self.process_voice_input(voice_output=voice_output_enabled)
                elif user_input.lower() in ['text-only', 't']:
                    voice_output_enabled = False
                    print("Voice output disabled. Responses will be text-only.")
                elif user_input.lower() in ['voice-on', 'vo']:
                    voice_output_enabled = True
                    print("Voice output enabled.")
                else:
                    # Regular text input
                    self.process_text_input(user_input, voice_output=voice_output_enabled)
            
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    try:
        assistant = MultimodalAIAssistant()
        assistant.run_interactive_mode()
    except Exception as e:
        print(f"Failed to initialize assistant: {e}")
