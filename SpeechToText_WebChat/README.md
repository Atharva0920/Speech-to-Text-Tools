# 💬 Web Voice Chat

Real-time voice-to-text chat application powered by Flask-SocketIO. Speak or type messages with automatic transcription and live broadcasting to all connected users.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.7+-green)
![Flask](https://img.shields.io/badge/flask-3.0+-red)
![License](https://img.shields.io/badge/license-MIT-orange)

## 🎯 Features

- 🎙️ **Voice-to-text** - Real-time speech transcription
- 💬 **Text chat** - Traditional text messaging
- 👥 **Multi-user** - Broadcasts to all connected clients
- 🔄 **Real-time** - Socket.IO for instant communication
- 🎨 **Modern UI** - Clean, responsive design
- 📱 **Mobile-friendly** - Works on phones and tablets
- 🌐 **Browser-based** - No installation required

## 🚀 Quick Start

### Basic Setup (No FFmpeg)

```bash
# Clone the repository
git clone https://github.com/yourusername/web-voice-chat.git
cd web-voice-chat

# Install dependencies
pip install flask flask-socketio speech_recognition python-socketio

# Run the server
python web_chat_example.py

# Open browser
http://localhost:5000
```

### Advanced Setup (With FFmpeg - Better Audio Quality)

```bash
# Install Python dependencies
pip install flask flask-socketio speech_recognition pydub python-socketio

# Install FFmpeg
# Windows: Download from https://www.gyan.dev/ffmpeg/builds/
# Extract and add bin folder to PATH

# macOS:
brew install ffmpeg

# Linux:
sudo apt-get install ffmpeg

# Run the server
python web_chat_example.py
```

## 📂 Project Structure

```
web-voice-chat/
├── web_chat_example.py          # Flask server
├── templates/
│   └── chat.html                # Frontend UI
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore                   # Git ignore rules
```

## 📖 Usage Guide

### Starting the Server

```bash
python web_chat_example.py
```

Server starts at `http://localhost:5000`

### Using the Chat Interface

1. **Open the application** in your browser
2. **Record voice message:**
   - Click "🎤 Start Recording"
   - Speak clearly (5-10 seconds recommended)
   - Click "⏹️ Stop Recording"
   - Text appears automatically
3. **Send text message:**
   - Type in the input field
   - Press Enter or click "Send"
4. **Clear messages:**
   - Click "🗑️ Clear" button

### Browser Permissions

First time:
- Browser will ask for microphone permission
- Click "Allow" to enable voice recording

## ⚙️ Configuration

### Change Server Port

Edit `web_chat_example.py` at the end:

```python
socketio.run(app, debug=True, host='0.0.0.0', port=5000)
#                                              ↑
#                                        Change port here
```

### Change Language

Edit line 78:

```python
text = r.recognize_google(audio_sr, language='en-US')
```

**Supported languages:**
- `'en-US'` - English (US)
- `'en-GB'` - English (UK)
- `'es-ES'` - Spanish
- `'fr-FR'` - French
- `'de-DE'` - German
- `'it-IT'` - Italian
- `'pt-BR'` - Portuguese (Brazil)
- `'ja-JP'` - Japanese
- `'zh-CN'` - Chinese (Simplified)
- `'hi-IN'` - Hindi

[Complete language list](https://cloud.google.com/speech-to-text/docs/languages)

### Audio Recording Settings

Edit `chat.html` around line 110:

```javascript
const stream = await navigator.mediaDevices.getUserMedia({ 
    audio: {
        channelCount: 1,        // Mono audio
        sampleRate: 16000,      // 16kHz sample rate
        echoCancellation: true, // Enable echo cancellation
        noiseSuppression: true  // Enable noise suppression
    } 
});
```

### Customize UI

Edit `templates/chat.html`:

**Change colors:**
```css
.btn-primary {
    background-color: #007bff;  /* Change button color */
}
```

**Change chat height:**
```css
.messages {
    height: 400px;  /* Adjust height */
}
```

## 🌐 Deployment

### Local Network Access

Allow other devices on your network:

```python
# Change host to 0.0.0.0
socketio.run(app, host='0.0.0.0', port=5000)
```

Access from other devices:
```
http://YOUR_IP_ADDRESS:5000
```

Find your IP:
```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
```

### Production Deployment

#### Using Gunicorn

```bash
# Install gunicorn
pip install gunicorn eventlet

# Run with gunicorn
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 web_chat_example:app
```

#### Deploy to Heroku

1. Create `Procfile`:
```
web: gunicorn --worker-class eventlet -w 1 web_chat_example:app
```

2. Create `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

#### Deploy to Railway

1. Connect your GitHub repository
2. Add build command: `pip install -r requirements.txt`
3. Add start command: `python web_chat_example.py`
4. Deploy!

### Environment Variables

For production, use environment variables:

```python
import os

# Secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Port
port = int(os.environ.get('PORT', 5000))
socketio.run(app, host='0.0.0.0', port=port)
```

## 🔌 API Reference

### Socket.IO Events

#### Client → Server

**Send Audio Data**
```javascript
socket.emit('audio_data', {
    audio: base64Audio,           // Base64 encoded audio
    format: 'webm',               // Audio format
    timestamp: '2024-01-01T12:00:00Z'
});
```

**Send Text Message**
```javascript
socket.emit('text_message', {
    text: 'Hello, world!',
    sender: 'Username',
    timestamp: '2024-01-01T12:00:00Z'
});
```

#### Server → Client

**Receive Transcription**
```javascript
socket.on('transcription', (data) => {
    if (data.success) {
        console.log('Transcribed:', data.text);
    } else {
        console.error('Error:', data.error);
    }
});
```

**Receive New Message**
```javascript
socket.on('new_message', (data) => {
    console.log(`${data.sender}: ${data.text}`);
    // data.timestamp also available
});
```

**Connection Events**
```javascript
socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});
```

### REST Endpoints

**Home Page**
```
GET /
Returns: HTML chat interface
```

## 🐛 Troubleshooting

### FFmpeg Not Found

**Error:** `FileNotFoundError: [WinError 2] The system cannot find the file specified`

**Solution:**
1. Install FFmpeg from https://www.gyan.dev/ffmpeg/builds/
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Restart terminal/IDE
5. Verify: `ffmpeg -version`

**Alternative:** Use the no-FFmpeg version (lower audio quality)

### Microphone Not Working

**Solutions:**
- Check browser permissions (should see microphone icon in address bar)
- Try different browser (Chrome recommended)
- Check Windows privacy settings → Microphone
- Ensure microphone is selected as default device

### Audio Not Transcribing

**Common issues:**
- **No internet:** Google Speech API requires internet
- **Too quiet:** Speak louder or closer to microphone
- **Too long:** Keep recordings under 10 seconds
- **Background noise:** Find quieter environment

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 5000
# Windows:
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID_NUMBER> /F

# Or change port in code
socketio.run(app, port=5001)  # Use different port
```

### Socket.IO Connection Failed

**Check:**
- Server is running
- Correct URL in browser
- No firewall blocking port
- CORS settings if accessing from different domain

**Fix CORS:**
```python
socketio = SocketIO(app, cors_allowed_origins="*")
```

### Build from Requirements Fails

```bash
# Update pip first
pip install --upgrade pip

# Install dependencies one by one
pip install flask
pip install flask-socketio
pip install speech_recognition
pip install python-socketio
pip install pydub  # Optional
```

## 🔒 Security Considerations

### Production Checklist

- [ ] Change secret key to random string
- [ ] Use environment variables for sensitive data
- [ ] Enable HTTPS/SSL
- [ ] Restrict CORS origins
- [ ] Add rate limiting
- [ ] Implement authentication
- [ ] Sanitize user inputs
- [ ] Add content security policy

### Example Secure Configuration

```python
import os
import secrets

# Strong secret key
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Restrict CORS
socketio = SocketIO(app, cors_allowed_origins=['https://yourdomain.com'])

# Add rate limiting
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)
```

## 📊 Performance Optimization

### Tips for Better Performance

1. **Use production server:**
   ```bash
   gunicorn --worker-class eventlet -w 1 web_chat_example:app
   ```

2. **Enable compression:**
   ```python
   from flask_compress import Compress
   Compress(app)
   ```

3. **CDN for static files:**
   ```html
   <script src="https://cdn.jsdelivr.net/npm/socket.io@4.7.2/client-dist/socket.io.min.js"></script>
   ```

4. **Limit recording duration:**
   ```javascript
   // In chat.html
   mediaRecorder.start();
   setTimeout(() => mediaRecorder.stop(), 10000);  // 10 sec max
   ```

## 🧪 Testing

### Manual Testing

1. Open multiple browser tabs/windows
2. Send message from one → should appear in all
3. Record voice → should transcribe and broadcast
4. Test with different browsers
5. Test on mobile devices

### Automated Testing (Future)

```bash
# Install testing dependencies
pip install pytest pytest-flask

# Run tests
pytest tests/
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

- **Flask** - Web framework
- **Flask-SocketIO** - Real-time communication
- **SpeechRecognition** - Speech-to-text
- **Socket.IO** - Bidirectional events
- **Google Speech API** - Speech recognition service

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/NewFeature`
3. Commit changes: `git commit -m 'Add NewFeature'`
4. Push to branch: `git push origin feature/NewFeature`
5. Open Pull Request

## 📧 Support

- 🐛 [Report Issues](https://github.com/yourusername/web-voice-chat/issues)
- 💡 [Feature Requests](https://github.com/yourusername/web-voice-chat/issues)
- 📖 [Documentation](https://github.com/yourusername/web-voice-chat/wiki)
- 💬 [Discussions](https://github.com/yourusername/web-voice-chat/discussions)

## 🗺️ Roadmap

- [ ] User authentication
- [ ] Private chat rooms
- [ ] Message history/persistence
- [ ] File sharing
- [ ] Emoji support
- [ ] Markdown formatting
- [ ] Voice message playback
- [ ] Desktop notifications
- [ ] Dark mode
- [ ] Multiple languages UI

## ⭐ Star History

If this project helped you, please consider giving it a star!

---

**Built with ❤️ for seamless communication**