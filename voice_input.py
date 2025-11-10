"""
Voice Input Module - Handles speech-to-text functionality
"""
import speech_recognition as sr

class VoiceInput:
    def __init__(self):
        """Initialize speech recognizer"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        
    def listen(self):
        """
        Listen to microphone and convert speech to text
        
        Returns:
            str: Recognized text or error message
        """
        try:
            with sr.Microphone() as source:
                print("🎤 Listening... (speak now)")
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=15)
                
                print("🔄 Processing speech...")
                
                # Convert speech to text using Google Speech Recognition
                text = self.recognizer.recognize_google(audio)
                
                return text
                
        except sr.WaitTimeoutError:
            return "ERROR: No speech detected. Please try again."
        except sr.UnknownValueError:
            return "ERROR: Could not understand the audio. Please speak clearly."
        except sr.RequestError as e:
            return f"ERROR: Could not request results from speech recognition service: {e}"
        except Exception as e:
            return f"ERROR: An unexpected error occurred: {e}"
    
    def listen_continuous(self, callback):
        """
        Listen continuously and call callback function with recognized text
        
        Args:
            callback: Function to call with recognized text
        """
        with sr.Microphone() as source:
            print("🎤 Continuous listening mode activated...")
            self.recognizer.adjust_for_ambient_noise(source)
            
            while True:
                try:
                    audio = self.recognizer.listen(source, timeout=None)
                    text = self.recognizer.recognize_google(audio)
                    callback(text)
                except KeyboardInterrupt:
                    print("\n🛑 Stopping continuous listening...")
                    break
                except sr.UnknownValueError:
                    continue
                except Exception as e:
                    print(f"Error: {e}")
                    continue
