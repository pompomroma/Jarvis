"""
Voice Output Module
Handles text-to-speech conversion
"""

import pyttsx3
import threading
from gtts import gTTS
import os
import tempfile
import platform

class VoiceOutput:
    def __init__(self, use_gtts=False):
        """
        Initialize voice output
        
        Args:
            use_gtts: If True, use Google TTS (requires internet), 
                     otherwise use pyttsx3 (offline)
        """
        self.use_gtts = use_gtts
        
        if not use_gtts:
            # Initialize pyttsx3 for offline TTS
            self.engine = pyttsx3.init()
            
            # Configure voice properties
            voices = self.engine.getProperty('voices')
            # Try to set a pleasant voice (usually index 1 is female on many systems)
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[1].id)
            
            # Set speech rate (default is usually 200)
            self.engine.setProperty('rate', 175)
            
            # Set volume (0.0 to 1.0)
            self.engine.setProperty('volume', 0.9)
    
    def speak(self, text):
        """
        Convert text to speech and play it
        
        Args:
            text: The text to speak
        """
        if not text:
            return
        
        print(f"🔊 Speaking: {text}")
        
        try:
            if self.use_gtts:
                self._speak_gtts(text)
            else:
                self._speak_pyttsx3(text)
        except Exception as e:
            print(f"❌ Error during text-to-speech: {e}")
    
    def _speak_pyttsx3(self, text):
        """Speak using pyttsx3 (offline)"""
        self.engine.say(text)
        self.engine.runAndWait()
    
    def _speak_gtts(self, text):
        """Speak using Google TTS (requires internet)"""
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
            temp_file = fp.name
        
        try:
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(temp_file)
            
            # Play the audio file
            if platform.system() == 'Darwin':  # macOS
                os.system(f'afplay {temp_file}')
            elif platform.system() == 'Linux':
                os.system(f'mpg123 {temp_file} 2>/dev/null || ffplay -nodisp -autoexit {temp_file} 2>/dev/null')
            else:  # Windows
                os.system(f'start {temp_file}')
                
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file)
            except:
                pass
    
    def speak_async(self, text):
        """
        Speak asynchronously (non-blocking)
        
        Args:
            text: The text to speak
        """
        thread = threading.Thread(target=self.speak, args=(text,))
        thread.daemon = True
        thread.start()
