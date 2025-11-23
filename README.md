# 🎤 Speech-to-Text Tools

A collection of powerful speech-to-text applications for voice input anywhere on your computer or in web applications.

## 📦 Projects

### 1. [Global Voice Input](#global-voice-input) - System-wide voice typing
Type with your voice in **any application** (Word, Notepad, browsers, etc.)

### 2. [Web Voice Chat](#web-voice-chat) - Real-time voice chat application
Browser-based voice-to-text chat with real-time transcription

---

## 🌍 Global Voice Input

A lightweight system tray application that enables voice typing anywhere on Windows using a global hotkey.

### ✨ Features

- 🎯 **System-wide hotkey** (`Ctrl+Alt+V`) - works in any application
- 🪟 **System tray integration** - runs silently in background
- 🎨 **Visual feedback** - icon changes color during recording
- ⚡ **Fast & lightweight** - minimal resource usage
- 🔒 **Privacy-focused** - audio processed via Google Speech API only

### 🚀 Quick Start

#### Option A: Run with Python

```bash
# Install dependencies
pip install SpeechRecognition pyautogui keyboard pystray pillow

# Run the application
python global_voice_input.py
```

#### Option B: Build Standalone Executable

```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
python build_exe.py

# Run the exe (no Python needed!)
dist/VoiceInput.exe
```

### 📖 Usage

1. **Start the application** - Look for microphone icon in system tray
2. **Click on any text field** (Word, Notepad, browser, etc.)
3. **Press `Ctrl+Alt+V`** and speak
4. **Your text appears automatically!**

### ⚙️ Auto-Start with Windows

```bash
python setup_autostart.py
```

Choose option 1 to add Voice Input to Windows startup.

### 🎯 Customization

**Change Hotkey:**
Edit `global_voice_input.py` line 55:
```python
keyboard.add_hotkey('ctrl+alt+v', on_hotkey)  # Change to your preference
```

**Popular alternatives:**
- `'ctrl+shift+space'` - Spacebar-based
- `'alt+v'` - Simple Alt+V
- `'f9'` - Function key

### 📋 Requirements

- Python 3.7+
- Windows 10/11
- Microphone
- Internet connection (for Google Speech API)

### 🐛 Troubleshooting

**Microphone not detected:**
```bash
# Test your microphone
python -m speech_recognition
```

**Hotkey not working:**
- Make sure no other app uses the same hotkey
- Run as administrator if needed

**Build errors:**
```bash
# Install all dependencies first
pip install --upgrade pyinstaller speech_recognition pyautogui keyboard pystray pillow
```

---

## 💬 Web Voice Chat

A Flask-SocketIO powered web application for real-time voice-to-text chat. Perfect for group conversations with voice transcription.

### ✨ Features

- 🎙️ **Real-time voice transcription** - speak and see text instantly
- 💬 **Text chat support** - type or speak
- 👥 **Multi-user support** - broadcasts to all connected clients
- 🎨 **Modern UI** - clean, responsive interface
- 🔄 **Socket.IO** - real-time bidirectional communication

### 🚀 Quick Start

#### Without FFmpeg (Simpler)

```bash
# Install dependencies
pip install flask flask-socketio speech_recognition python-socketio

# Run the application
python web_chat_example.py

# Open browser
http://localhost:5000
```

#### With FFmpeg (Better Audio Quality)

```bash
# Install dependencies
pip install flask flask-socketio speech_recognition pydub python-socketio

# Install FFmpeg
# Windows: Download from https://www.gyan.dev/ffmpeg/builds/
# Add to PATH: C:\ffmpeg\bin

# Run the application
python web_chat_example.py
```

### 📖 Usage

1. **Start the server** - Run the Python script
2. **Open browser** - Navigate to `http://localhost:5000`
3. **Click "Start Recording"** - Speak clearly
4. **Click "Stop Recording"** - Text appears automatically
5. **Type messages** - Use input field for text chat

### 🏗️ Project Structure

```
web-voice-chat/
├── web_chat_example.py          # Main Flask application
├── templates/
│   └── chat.html                # Frontend interface
├── requirements.txt             # Python dependencies
└── README.md                    # Documentation
```

### ⚙️ Configuration

**Change Port:**
```python
socketio.run(app, debug=True, host='0.0.0.0', port=5000)  # Change port here
```

**Change Language:**
```python
text = r.recognize_google(audio_sr, language='en-US')  # Change language code
```

**Supported languages:**
- `'en-US'` - English (US)
- `'es-ES'` - Spanish
- `'fr-FR'` - French
- `'de-DE'` - German
- [See full list](https://cloud.google.com/speech-to-text/docs/languages)

### 📋 API Reference

#### Socket.IO Events

**Client → Server:**
```javascript
// Send audio data
socket.emit('audio_data', {
    audio: base64Audio,
    format: 'webm',
    timestamp: new Date().toISOString()
});

// Send text message
socket.emit('text_message', {
    text: 'Hello',
    sender: 'User',
    timestamp: new Date().toISOString()
});
```

**Server → Client:**
```javascript
// Receive transcription
socket.on('transcription', (data) => {
    // data.success, data.text, data.error
});

// Receive new message
socket.on('new_message', (data) => {
    // data.text, data.sender, data.timestamp
});
```

### 🌐 Deployment

#### Local Network

```python
# Allow access from other devices
socketio.run(app, host='0.0.0.0', port=5000)

# Access from other devices
http://YOUR_IP_ADDRESS:5000
```

#### Production (Heroku/Railway/etc.)

```python
# Use environment variables
import os
port = int(os.environ.get('PORT', 5000))
socketio.run(app, host='0.0.0.0', port=port)
```

### 🐛 Troubleshooting

**"FFmpeg not found" error:**
- Install FFmpeg and add to PATH
- OR use the no-FFmpeg version

**Audio not transcribing:**
- Check microphone permissions in browser
- Ensure internet connection (Google API needs internet)
- Try shorter recordings (5-10 seconds)

**CORS errors:**
- Check `cors_allowed_origins="*"` in SocketIO config
- For production, specify allowed origins

---

## 📦 Dependencies

### Global Voice Input
```txt
SpeechRecognition>=3.10.0
PyAudio>=0.2.13
pyautogui>=0.9.54
keyboard>=0.13.5
pystray>=0.19.4
Pillow>=10.0.0
```

### Web Voice Chat
```txt
Flask>=3.0.0
flask-socketio>=5.3.0
python-socketio>=5.10.0
SpeechRecognition>=3.10.0
pydub>=0.25.1  # Optional, for FFmpeg support
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Speech recognition library
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/) - Real-time communication
- [pystray](https://github.com/moses-palmer/pystray) - System tray integration
- Google Speech Recognition API

## 📧 Support

- 🐛 [Report Bug](https://github.com/yourusername/speech-to-text-tools/issues)
- 💡 [Request Feature](https://github.com/yourusername/speech-to-text-tools/issues)
- 📖 [Documentation](https://github.com/yourusername/speech-to-text-tools/wiki)

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

Made with ❤️ by Atharva Ganmote
