"""
Voice Output Module - Handles text-to-speech functionality
"""
import pyttsx3
import threading

class VoiceOutput:
    def __init__(self):
        """Initialize text-to-speech engine"""
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Get available voices and set a good one
        voices = self.engine.getProperty('voices')
        if len(voices) > 0:
            # Try to set a nice voice (usually the first or second voice is good)
            self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text, async_mode=False):
        """
        Convert text to speech
        
        Args:
            text (str): Text to speak
            async_mode (bool): If True, speak in a separate thread (non-blocking)
        """
        if async_mode:
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text):
        """Internal method to speak text synchronously"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Error in speech synthesis: {e}")
    
    def stop(self):
        """Stop speaking"""
        try:
            self.engine.stop()
        except:
            pass
    
    def set_voice_properties(self, rate=None, volume=None):
        """
        Adjust voice properties
        
        Args:
            rate (int): Speech rate (words per minute)
            volume (float): Volume level (0.0 to 1.0)
        """
        if rate:
            self.engine.setProperty('rate', rate)
        if volume:
            self.engine.setProperty('volume', volume)
    
    def list_voices(self):
        """List available voices"""
        voices = self.engine.getProperty('voices')
        for idx, voice in enumerate(voices):
            print(f"{idx}: {voice.name} ({voice.id})")
        return voices
    
    def change_voice(self, voice_index):
        """
        Change the voice
        
        Args:
            voice_index (int): Index of the voice to use
        """
        voices = self.engine.getProperty('voices')
        if 0 <= voice_index < len(voices):
            self.engine.setProperty('voice', voices[voice_index].id)
            return True
        return False
