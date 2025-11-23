import telebot
import speech_recognition as sr
import tempfile
import os

# Initialize bot with your token
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')
r = sr.Recognizer()

@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    """Handle voice messages in Telegram"""
    try:
        # Get file info
        file_info = bot.get_file(message.voice.file_id)
        
        # Download the voice file
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.ogg', delete=False) as temp_file:
            temp_file.write(downloaded_file)
            temp_filename = temp_file.name
        
        # Convert to text
        text = convert_telegram_audio_to_text(temp_filename)
        
        # Send response
        if text:
            bot.reply_to(message, f"🎤 *Transcription:*\n{text}", parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ Sorry, I couldn't understand the audio.")
        
        # Clean up
        os.unlink(temp_filename)
        
    except Exception as e:
        bot.reply_to(message, f"❌ Error processing voice message: {str(e)}")

@bot.message_handler(content_types=['audio', 'document'])
def handle_audio_files(message):
    """Handle audio files and documents"""
    try:
        file_id = None
        
        if message.audio:
            file_id = message.audio.file_id
        elif message.document and message.document.mime_type.startswith('audio/'):
            file_id = message.document.file_id
        
        if file_id:
            # Similar processing as voice messages
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(downloaded_file)
                temp_filename = temp_file.name
            
            text = convert_telegram_audio_to_text(temp_filename)
            
            if text:
                bot.reply_to(message, f"🎤 *Transcription:*\n{text}", parse_mode='Markdown')
            else:
                bot.reply_to(message, "❌ Sorry, I couldn't understand the audio.")
            
            os.unlink(temp_filename)
            
    except Exception as e:
        bot.reply_to(message, f"❌ Error processing audio: {str(e)}")

def convert_telegram_audio_to_text(audio_file_path):
    """Convert audio file to text"""
    try:
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)
            text = r.recognize_google(audio)
            return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Welcome message"""
    welcome_text = """
🎤 *Speech to Text Bot*

Send me a voice message or audio file, and I'll transcribe it to text!

Supported formats:
• Voice messages
• Audio files (MP3, WAV, etc.)
    """
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

if __name__ == '__main__':
    print("Bot is running...")
    bot.polling(none_stop=True)