import speech_recognition as sr
import pyttsx3
import threading
import queue
from typing import Optional

class VoiceHandler:
    def __init__(self):
        """Initialize voice input and output handlers."""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.audio_queue = queue.Queue()
        
        # Configure TTS
        self._configure_tts()
        
        # Calibrate microphone for ambient noise
        print("Calibrating microphone for ambient noise... Please wait.")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Microphone calibrated!")
    
    def _configure_tts(self):
        """Configure text-to-speech engine."""
        # Set speech rate (words per minute)
        self.tts_engine.setProperty('rate', 150)
        
        # Set volume (0.0 to 1.0)
        self.tts_engine.setProperty('volume', 0.9)
        
        # Try to set a better voice if available
        voices = self.tts_engine.getProperty('voices')
        if voices:
            # Prefer female voice if available, otherwise use first available
            for voice in voices:
                if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    break
            else:
                self.tts_engine.setProperty('voice', voices[0].id)
    
    def listen(self, timeout: int = 5, phrase_time_limit: int = 10) -> Optional[str]:
        """
        Listen for voice input and convert to text.
        
        Args:
            timeout: Maximum time to wait for speech to start
            phrase_time_limit: Maximum time for a phrase
            
        Returns:
            Transcribed text or None if no speech detected
        """
        try:
            with self.microphone as source:
                print("Listening... (speak now)")
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("Processing speech...")
            try:
                # Use Google's speech recognition (free, no API key needed)
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text
            except sr.UnknownValueError:
                print("Could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Error with speech recognition service: {e}")
                return None
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout period")
            return None
        except Exception as e:
            print(f"Error listening: {e}")
            return None
    
    def speak(self, text: str):
        """Convert text to speech and speak it."""
        try:
            print(f"AI: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"Error speaking: {e}")
    
    def speak_async(self, text: str):
        """Speak text asynchronously in a separate thread."""
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
