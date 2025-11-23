from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import speech_recognition as sr
import base64
import os
from pydub import AudioSegment
from datetime import datetime
import tempfile
import logging
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24))
socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=10e6)

# Initialize speech recognizer
r = sr.Recognizer()
r.energy_threshold = 4000
r.dynamic_energy_threshold = True

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('audio_data')
def handle_audio(data):
    """Handle incoming audio data from web client"""
    try:
        logger.info("Received audio data for transcription")
        
        # Decode base64 audio data
        audio_data = base64.b64decode(data['audio'])
        
        # Convert to text (handles both webm and wav formats)
        text = convert_audio_to_text(audio_data)
        
        if text:
            logger.info(f"Transcription successful: {text}")
            # Send transcription back to client
            emit('transcription', {
                'success': True,
                'text': text,
                'timestamp': data.get('timestamp', datetime.now().isoformat())
            })
            
            # Broadcast as a message to all clients
            emit('new_message', {
                'text': text,
                'sender': 'Voice User',
                'timestamp': data.get('timestamp', datetime.now().isoformat())
            }, broadcast=True)
        else:
            logger.warning("Could not understand audio")
            emit('transcription', {
                'success': False,
                'error': 'Could not understand audio. Please speak clearly and try again.'
            })
            
    except Exception as e:
        logger.error(f"Audio handling error: {str(e)}", exc_info=True)
        emit('transcription', {
            'success': False,
            'error': f'Error processing audio: {str(e)}'
        })

@socketio.on('text_message')
def handle_message(data):
    """Handle regular text messages"""
    logger.info(f"Received text message from {data.get('sender', 'Unknown')}")
    emit('new_message', {
        'text': data['text'],
        'sender': data.get('sender', 'User'),
        'timestamp': data.get('timestamp', datetime.now().isoformat())
    }, broadcast=True)

def convert_audio_to_text(audio_data):
    """
    Convert audio data to text using Google Speech Recognition
    Handles multiple audio formats (webm, wav, etc.)
    """
    temp_input_path = None
    temp_wav_path = None
    
    try:
        logger.info(f"Received audio data: {len(audio_data)} bytes")
        
        # Verify we have data
        if len(audio_data) == 0:
            logger.error("Received empty audio data")
            return None
        
        # Create temporary file for input audio and ensure it's written
        temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.webm', mode='wb')
        temp_input.write(audio_data)
        temp_input.flush()  # Ensure data is written to disk
        temp_input.close()  # Close the file so other processes can access it
        temp_input_path = temp_input.name
        
        logger.info(f"Created temp file: {temp_input_path}, size: {os.path.getsize(temp_input_path)} bytes")
        
        # Verify file was created
        if not os.path.exists(temp_input_path):
            logger.error(f"Temp file not created: {temp_input_path}")
            return None
        
        # Try to detect and convert audio format
        try:
            # Attempt to load as webm first (most common from browsers)
            logger.info("Attempting to load as WebM...")
            audio = AudioSegment.from_file(temp_input_path, format='webm')
            logger.info("Successfully loaded as WebM")
        except Exception as e1:
            logger.warning(f"Failed to load as WebM: {e1}")
            try:
                # Try as wav
                logger.info("Attempting to load as WAV...")
                audio = AudioSegment.from_file(temp_input_path, format='wav')
                logger.info("Successfully loaded as WAV")
            except Exception as e2:
                logger.warning(f"Failed to load as WAV: {e2}")
                try:
                    # Let pydub auto-detect format
                    logger.info("Attempting auto-detect format...")
                    audio = AudioSegment.from_file(temp_input_path)
                    logger.info("Successfully loaded with auto-detect")
                except Exception as e3:
                    logger.error(f"Failed all audio loading attempts: {e3}")
                    raise e3
        
        logger.info(f"Audio loaded: duration={len(audio)}ms, channels={audio.channels}, frame_rate={audio.frame_rate}")
        
        # Convert to optimal format for speech recognition
        # Mono audio, 16kHz sample rate, 16-bit
        audio = audio.set_channels(1)
        audio = audio.set_frame_rate(16000)
        audio = audio.set_sample_width(2)
        
        # Export to WAV format
        temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix='.wav', mode='wb')
        temp_wav.close()  # Close immediately so pydub can write to it
        temp_wav_path = temp_wav.name
        
        audio.export(temp_wav_path, format='wav')
        logger.info(f"Exported to WAV: {temp_wav_path}")
        
        # Use speech recognition
        with sr.AudioFile(temp_wav_path) as source:
            # Adjust for ambient noise
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio_data_sr = r.record(source)
            
        # Recognize speech using Google Speech Recognition
        text = r.recognize_google(audio_data_sr, language='en-US')
        logger.info(f"Recognition successful: {text}")
        return text
        
    except sr.UnknownValueError:
        logger.warning("Speech recognition could not understand audio")
        return None
    except sr.RequestError as e:
        logger.error(f"Speech recognition service error: {e}")
        return None
    except Exception as e:
        logger.error(f"Error in audio conversion: {str(e)}", exc_info=True)
        return None
    finally:
        # Cleanup temporary files
        cleanup_files([temp_input_path, temp_wav_path])

def cleanup_files(file_paths):
    """Clean up temporary files"""
    for path in file_paths:
        if path and os.path.exists(path):
            try:
                os.unlink(path)
                logger.debug(f"Cleaned up temp file: {path}")
            except Exception as e:
                logger.error(f"Error cleaning up {path}: {e}")

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    logger.info(f"Client connected: {request.sid}")
    emit('connection_response', {'status': 'connected'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {request.sid}")

@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler"""
    logger.error(f"Application error: {str(error)}", exc_info=True)
    return {'error': str(error)}, 500

if __name__ == '__main__':
    logger.info("Starting Flask-SocketIO server...")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)