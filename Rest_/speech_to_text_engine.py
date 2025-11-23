import speech_recognition as sr
import pyttsx3
import threading
import time
from datetime import datetime
import json

class SpeechToTextEngine:
    """Modular Speech to Text engine that can be integrated into any application"""
    
    def __init__(self, output_file="output.txt", use_tts=True):
        self.recognizer = sr.Recognizer()
        self.output_file = output_file
        self.use_tts = use_tts
        self.is_listening = False
        self.callbacks = []
        
        if use_tts:
            self.tts_engine = pyttsx3.init()
    
    def add_callback(self, callback):
        """Add a callback function to be called when text is recognized"""
        self.callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Remove a callback function"""
        if callback in self.callbacks:
            self.callbacks.remove(callback)
    
    def _notify_callbacks(self, text, confidence=None):
        """Notify all registered callbacks"""
        for callback in self.callbacks:
            try:
                callback(text, confidence)
            except Exception as e:
                print(f"Error in callback: {e}")
    
    def record_text_once(self, timeout=5, phrase_timeout=1):
        """Record and convert speech to text once"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.2)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_timeout=phrase_timeout)
                
                print("Processing...")
                text = self.recognizer.recognize_google(audio, show_all=False)
                
                print(f"You said: {text}")
                return text
                
        except sr.WaitTimeoutError:
            print("No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
    
    def start_continuous_listening(self):
        """Start continuous listening in a separate thread"""
        if not self.is_listening:
            self.is_listening = True
            self.listen_thread = threading.Thread(target=self._continuous_listen)
            self.listen_thread.daemon = True
            self.listen_thread.start()
            print("Started continuous listening...")
    
    def stop_continuous_listening(self):
        """Stop continuous listening"""
        self.is_listening = False
        print("Stopped continuous listening...")
    
    def _continuous_listen(self):
        """Internal method for continuous listening"""
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            
        while self.is_listening:
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source, timeout=1, phrase_timeout=1)
                
                # Process in background to avoid blocking
                threading.Thread(target=self._process_audio, args=(audio,), daemon=True).start()
                
            except sr.WaitTimeoutError:
                continue
            except Exception as e:
                print(f"Error in continuous listening: {e}")
                time.sleep(0.1)
    
    def _process_audio(self, audio):
        """Process audio in background thread"""
        try:
            text = self.recognizer.recognize_google(audio)
            timestamp = datetime.now().isoformat()
            
            print(f"[{timestamp}] You said: {text}")
            
            # Save to file
            self.output_text(text, timestamp)
            
            # Notify callbacks
            self._notify_callbacks(text)
            
            # Text to speech (optional)
            if self.use_tts:
                self.speak(f"You said: {text}")
                
        except sr.UnknownValueError:
            pass  # Ignore unrecognized speech in continuous mode
        except sr.RequestError as e:
            print(f"Speech recognition error: {e}")
    
    def output_text(self, text, timestamp=None):
        """Save text to output file with timestamp"""
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        # Save as JSON for better structure
        entry = {
            "timestamp": timestamp,
            "text": text
        }
        
        try:
            with open(self.output_file, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"Error saving to file: {e}")
    
    def speak(self, text):
        """Convert text to speech"""
        if self.use_tts:
            try:
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
            except Exception as e:
                print(f"TTS error: {e}")
    
    def process_audio_file(self, file_path):
        """Process an audio file and return the text"""
        try:
            with sr.AudioFile(file_path) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return None

# Example usage and integration patterns
if __name__ == "__main__":
    # Create engine instance
    engine = SpeechToTextEngine(output_file="structured_output.txt")
    
    # Example callback for chat integration
    def chat_callback(text, confidence=None):
        """Example callback that could send to chat API"""
        print(f"CHAT: New message - {text}")
        # Here you would integrate with your chat API
        # send_to_discord(text)
        # send_to_telegram(text)
        # send_to_whatsapp(text)
    
    # Add callback
    engine.add_callback(chat_callback)
    
    print("Speech to Text Engine")
    print("1. Press Enter for single recording")
    print("2. Type 'start' for continuous listening")
    print("3. Type 'stop' to stop continuous listening")
    print("4. Type 'quit' to exit")
    
    while True:
        command = input("\nEnter command: ").strip().lower()
        
        if command == "":
            # Single recording
            text = engine.record_text_once()
            if text:
                engine.output_text(text)
        
        elif command == "start":
            engine.start_continuous_listening()
        
        elif command == "stop":
            engine.stop_continuous_listening()
        
        elif command == "quit":
            engine.stop_continuous_listening()
            break
        
        else:
            print("Unknown command")