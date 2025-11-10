"""
Voice Input Module
Handles speech-to-text conversion using speech recognition
"""

import speech_recognition as sr

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
    def listen(self, timeout=5, phrase_time_limit=10):
        """
        Listen to microphone and convert speech to text
        
        Args:
            timeout: Maximum time to wait for speech to start (seconds)
            phrase_time_limit: Maximum time for a single phrase (seconds)
        
        Returns:
            Recognized text or None if recognition failed
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... Speak now!")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                
                print("🔄 Processing speech...")
                
                # Recognize speech using Google's speech recognition
                text = self.recognizer.recognize_google(audio)
                print(f"📝 You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("❌ No speech detected. Please try again.")
            return None
        except sr.UnknownValueError:
            print("❌ Could not understand audio. Please speak clearly.")
            return None
        except sr.RequestError as e:
            print(f"❌ Could not request results from speech recognition service; {e}")
            return None
        except Exception as e:
            print(f"❌ Error during speech recognition: {e}")
            return None
    
    def listen_with_retry(self, max_retries=3):
        """
        Listen with automatic retries
        
        Args:
            max_retries: Maximum number of retry attempts
        
        Returns:
            Recognized text or None if all attempts failed
        """
        for attempt in range(max_retries):
            result = self.listen()
            if result:
                return result
            if attempt < max_retries - 1:
                print(f"🔄 Retry {attempt + 1}/{max_retries - 1}...")
        
        return None
