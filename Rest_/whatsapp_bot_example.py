from flask import Flask, request
import speech_recognition as sr
import requests
import tempfile
import os

app = Flask(__name__)
r = sr.Recognizer()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    data = request.get_json()
    
    # Check if it's an audio message
    if 'audio' in data.get('message', {}):
        audio_url = data['message']['audio']['url']
        sender = data['message']['from']
        
        # Download and process audio
        text = process_whatsapp_audio(audio_url)
        
        if text:
            # Send transcription back
            send_whatsapp_message(sender, f"🎤 Transcription: {text}")
        else:
            send_whatsapp_message(sender, "❌ Could not understand the audio.")
    
    return 'OK'

def process_whatsapp_audio(audio_url):
    """Download and convert WhatsApp audio to text"""
    try:
        # Download audio file
        response = requests.get(audio_url)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
            temp_file.write(response.content)
            temp_filename = temp_file.name
        
        # Convert to text
        with sr.AudioFile(temp_filename) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
        
        # Clean up
        os.unlink(temp_filename)
        return text
        
    except Exception as e:
        print(f"Error processing audio: {e}")
        return None

def send_whatsapp_message(to, message):
    """Send message back via WhatsApp API"""
    # Implementation depends on your WhatsApp API provider
    # (Twilio, WhatsApp Business API, etc.)
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5000)