"""
Global Voice Input Tool - System Tray Version
Press alt+v to record voice and type anywhere
Runs silently in the background with system tray icon
"""

import speech_recognition as sr
import pyautogui
import keyboard
import threading
import time
import sys
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw

class GlobalVoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.icon = None
        
        # Setup system tray icon
        self.setup_tray_icon()
        
        # Register global hotkey
        self.setup_hotkey()
        
        print("Voice Input Ready! Press alt+v anywhere to record.")
        print("Running in system tray. Right-click the icon to quit.")
    
    def create_icon_image(self, color="blue"):
        """Create a simple microphone icon"""
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        if color == "blue":
            fill_color = (0, 123, 255)
        elif color == "red":
            fill_color = (220, 53, 69)
        else:
            fill_color = (40, 167, 69)
        
        # Draw microphone shape
        draw.ellipse([22, 15, 42, 35], fill=fill_color)
        draw.rectangle([28, 30, 36, 45], fill=fill_color)
        draw.arc([20, 35, 44, 50], 180, 360, fill=fill_color, width=3)
        draw.line([32, 50, 32, 55], fill=fill_color, width=3)
        draw.line([25, 55, 39, 55], fill=fill_color, width=3)
        
        return image
    
    def setup_tray_icon(self):
        """Setup system tray icon"""
        icon_image = self.create_icon_image()
        
        menu = Menu(
            MenuItem('Voice Input (alt+v)', self.show_status, default=True),
            MenuItem('Record Now', self.start_recording_from_menu),
            Menu.SEPARATOR,
            MenuItem('Quit', self.quit_app)
        )
        
        self.icon = Icon("voice_input", icon_image, "Voice Input - Ready", menu)
    
    def setup_hotkey(self):
        """Setup global hotkey listener"""
        def on_hotkey():
            if not self.is_recording:
                threading.Thread(target=self.start_recording, daemon=True).start()
        
        # Register alt+v
        keyboard.add_hotkey('alt+v', on_hotkey)
    
    def start_recording_from_menu(self, icon=None, item=None):
        """Start recording from menu click"""
        if not self.is_recording:
            threading.Thread(target=self.start_recording, daemon=True).start()
    
    def start_recording(self):
        """Start recording audio"""
        if self.is_recording:
            return
        
        self.is_recording = True
        self.update_icon_status("recording")
        print("🎤 Recording...")
        
        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                
                # Record for 5 seconds (or until silence)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
                self.update_icon_status("processing")
                print("⏳ Processing...")
                
                # Recognize speech
                text = self.recognizer.recognize_google(audio)
                
                # Type the text where cursor is
                self.type_text(text)
                
                print(f"✅ Typed: {text}")
                self.update_icon_status("success")
                
        except sr.WaitTimeoutError:
            print("⚠️ No speech detected")
            self.update_icon_status("ready")
        except sr.UnknownValueError:
            print("⚠️ Could not understand audio")
            self.update_icon_status("ready")
        except sr.RequestError as e:
            print(f"❌ Error: {str(e)}")
            self.update_icon_status("ready")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            self.update_icon_status("ready")
        finally:
            self.is_recording = False
            # Reset icon after 2 seconds
            time.sleep(2)
            self.update_icon_status("ready")
    
    def type_text(self, text):
        """Type text at current cursor position"""
        time.sleep(0.1)  # Small delay to ensure focus
        pyautogui.write(text, interval=0.01)
    
    def update_icon_status(self, status):
        """Update tray icon based on status"""
        if not self.icon:
            return
        
        if status == "recording":
            self.icon.icon = self.create_icon_image("red")
            self.icon.title = "Voice Input - Recording..."
        elif status == "processing":
            self.icon.icon = self.create_icon_image("blue")
            self.icon.title = "Voice Input - Processing..."
        elif status == "success":
            self.icon.icon = self.create_icon_image("green")
            self.icon.title = "Voice Input - Success!"
        else:  # ready
            self.icon.icon = self.create_icon_image("blue")
            self.icon.title = "Voice Input - Ready (alt+v)"
    
    def show_status(self, icon=None, item=None):
        """Show status message"""
        status = "Recording..." if self.is_recording else "Ready - Press alt+v"
        print(f"Status: {status}")
    
    def quit_app(self, icon=None, item=None):
        """Quit application"""
        print("Shutting down...")
        keyboard.unhook_all()
        if self.icon:
            self.icon.stop()
        sys.exit(0)
    
    def run(self):
        """Run the application"""
        # Run the tray icon (this blocks)
        self.icon.run()


if __name__ == "__main__":
    print("=" * 50)
    print("Global Voice Input - System Tray Mode")
    print("=" * 50)
    print("\n✅ Hotkey: alt+v")
    print("📍 Running in system tray (check taskbar)")
    print("💡 Click on text field before using hotkey")
    print("🔴 Right-click tray icon to quit\n")
    
    app = GlobalVoiceInput()
    app.run()