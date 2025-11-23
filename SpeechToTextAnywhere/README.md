# 🎤 Global Voice Input

Type with your voice **anywhere** on Windows using a simple hotkey. Works in Word, Notepad, browsers, and any text field system-wide.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Features

- ✅ **System-wide hotkey** - Works in ANY application
- 🪟 **System tray app** - Runs silently in background
- 🎨 **Visual status** - Icon changes color (Blue→Red→Green)
- ⚡ **Lightning fast** - Instant transcription
- 🔒 **Privacy-focused** - No data stored locally
- 🚀 **Auto-start** - Launch with Windows
- 📦 **Portable** - Single .exe file, no installation

## 🖼️ Screenshots

```
System Tray Icon States:
🔵 Blue   = Ready to record
🔴 Red    = Recording your voice
🟢 Green  = Successfully transcribed
```

## 🚀 Installation

### Method 1: Quick Start (Python)

```bash
# Clone the repository
git clone https://github.com/yourusername/global-voice-input.git
cd global-voice-input

# Install dependencies
pip install -r requirements.txt

# Run the application
python global_voice_input.py
```

### Method 2: Standalone Executable (No Python Required)

```bash
# Build the executable
pip install pyinstaller
python build_exe.py

# The executable will be in dist/VoiceInput.exe
# Just double-click to run!
```

### Method 3: Download Pre-built Release

1. Go to [Releases](https://github.com/yourusername/global-voice-input/releases)
2. Download `VoiceInput.exe`
3. Double-click to run
4. Allow microphone access when prompted

## 📖 How to Use

### Basic Usage

1. **Start the application**
   - Look for the microphone icon in your system tray (bottom-right)

2. **Position your cursor**
   - Click in any text field where you want to type

3. **Activate voice input**
   - Press `Ctrl+Alt+V`
   - Speak clearly (5-10 seconds)
   - Recording stops automatically after silence

4. **Your text appears!**
   - Text is typed automatically where your cursor was

### Alternative Recording Methods

- **Right-click tray icon** → "Record Now"
- Use the hotkey from anywhere

### Exiting the Application

- **Right-click tray icon** → "Quit"
- The app will stop and remove from system tray

## ⚙️ Configuration

### Change Hotkey

Edit `global_voice_input.py` at line 55:

```python
keyboard.add_hotkey('ctrl+alt+v', on_hotkey)
```

**Popular alternatives:**
```python
keyboard.add_hotkey('ctrl+shift+space', on_hotkey)  # Ctrl+Shift+Space
keyboard.add_hotkey('alt+v', on_hotkey)              # Alt+V
keyboard.add_hotkey('f9', on_hotkey)                 # F9 key
keyboard.add_hotkey('ctrl+grave', on_hotkey)         # Ctrl+` (backtick)
```

### Recording Duration

Edit line 71 for custom timeout:

```python
audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
#                                       ↑                          ↑
#                              Wait time (sec)          Max recording (sec)
```

### Language Support

Edit line 78 to change language:

```python
text = self.recognizer.recognize_google(audio, language='en-US')
```

**Supported languages:**
- `'en-US'` - English (United States)
- `'en-GB'` - English (United Kingdom)
- `'es-ES'` - Spanish (Spain)
- `'fr-FR'` - French (France)
- `'de-DE'` - German (Germany)
- `'it-IT'` - Italian (Italy)
- `'pt-BR'` - Portuguese (Brazil)
- `'ru-RU'` - Russian (Russia)
- `'ja-JP'` - Japanese (Japan)
- `'zh-CN'` - Chinese (Mandarin, Simplified)
- `'hi-IN'` - Hindi (India)

[Full language list](https://cloud.google.com/speech-to-text/docs/languages)

## 🔧 Advanced Features

### Auto-Start with Windows

```bash
python setup_autostart.py
```

Choose option 1 to add to startup. The app will launch automatically when Windows starts.

**Manual method:**
1. Press `Win+R`
2. Type: `shell:startup`
3. Copy `VoiceInput.exe` to this folder

### Run Minimized

The app automatically runs in system tray with no visible window.

### Building from Source

```bash
# Install build dependencies
pip install pyinstaller

# Build single executable
python build_exe.py

# Output: dist/VoiceInput.exe
```

**Custom build options:**

```bash
# With custom icon
pyinstaller --onefile --windowed --name=VoiceInput --icon=myicon.ico global_voice_input.py

# Debug mode (shows console)
pyinstaller --onefile --name=VoiceInput global_voice_input.py
```

## 📋 Requirements

### Minimum Requirements
- **OS:** Windows 10 or later
- **Python:** 3.7+ (if running from source)
- **RAM:** 100 MB
- **Internet:** Required for speech recognition

### Hardware Requirements
- **Microphone:** Any USB or built-in microphone
- **Audio:** Working audio input device

## 🐛 Troubleshooting

### Microphone Not Working

**Test your microphone:**
```bash
python -m speech_recognition
```

**Common fixes:**
- Check Windows microphone permissions
- Ensure microphone is set as default device
- Update audio drivers
- Try a different USB port (for USB mics)

### Hotkey Not Working

**Possible causes:**
- Another application using the same hotkey
- Keyboard hook not registering

**Solutions:**
- Change to a different hotkey
- Run as administrator
- Check Task Manager for conflicting apps

### "No Speech Detected" Error

**Tips for better recognition:**
- Speak clearly and at normal pace
- Reduce background noise
- Position microphone 6-12 inches from mouth
- Increase recording timeout in settings

### Build Errors

**Missing dependencies:**
```bash
pip install --upgrade pyinstaller SpeechRecognition pyautogui keyboard pystray pillow
```

**PyInstaller issues:**
```bash
# Clean build
pyinstaller --clean --onefile --windowed global_voice_input.py
```

### Application Won't Start

**Check Python version:**
```bash
python --version  # Should be 3.7 or higher
```

**Verify all packages installed:**
```bash
pip list | grep -E "SpeechRecognition|pyautogui|keyboard|pystray"
```

**Run with debug output:**
```bash
python global_voice_input.py
# Check console for error messages
```

## 🔒 Privacy & Security

- **No local storage** - Audio is not saved to disk
- **No cloud storage** - Text is not stored remotely
- **Google Speech API** - Audio sent only to Google for transcription
- **No telemetry** - No usage data collected
- **Open source** - Audit the code yourself

### Data Flow
1. Microphone → Captured temporarily in memory
2. Memory → Sent to Google Speech Recognition API
3. API → Returns text
4. Text → Typed at cursor position
5. All data cleared from memory

## 🤝 Contributing

Contributions welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit** your changes
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push** to the branch
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open** a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/global-voice-input.git
cd global-voice-input

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SpeechRecognition](https://github.com/Uberi/speech_recognition) by Anthony Zhang
- [pystray](https://github.com/moses-palmer/pystray) by Moses Palmér
- [keyboard](https://github.com/boppreh/keyboard) by BoppreH
- Google Speech Recognition API

## 📊 Changelog

### v1.0.0 (2024-01-XX)
- ✨ Initial release
- 🎤 Voice typing with system-wide hotkey
- 🪟 System tray integration
- 🎨 Visual status indicators
- 🚀 Auto-start support

## 🗺️ Roadmap

- [ ] Offline speech recognition
- [ ] Custom wake words
- [ ] Multi-language auto-detection
- [ ] Punctuation commands ("period", "comma")
- [ ] Custom vocabulary
- [ ] Voice commands (edit, delete, undo)
- [ ] macOS and Linux support

## 📧 Support

- 🐛 [Report Bug](https://github.com/yourusername/global-voice-input/issues)
- 💡 [Request Feature](https://github.com/yourusername/global-voice-input/issues)
- 💬 [Discussions](https://github.com/yourusername/global-voice-input/discussions)

## ⭐ Show Your Support

Give a ⭐ if this project helped you!

---

**Made with ❤️ for productive typing**