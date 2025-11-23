import discord
from discord.ext import commands
import speech_recognition as sr
import pyttsx3
import asyncio
import io
import wave

# Discord bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

r = sr.Recognizer()
engine = pyttsx3.init()

@bot.command()
async def voice_to_text(ctx):
    """Command to convert voice message to text"""
    await ctx.send("Please upload an audio file and I'll convert it to text!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # Check if message has audio attachment
    if message.attachments:
        for attachment in message.attachments:
            if attachment.content_type and attachment.content_type.startswith('audio/'):
                try:
                    # Download the audio file
                    audio_data = await attachment.read()
                    
                    # Convert to text
                    text = await convert_audio_to_text(audio_data)
                    
                    if text:
                        embed = discord.Embed(
                            title="🎤 Speech to Text",
                            description=f"**Transcription:**\n{text}",
                            color=0x00ff00
                        )
                        await message.reply(embed=embed)
                    else:
                        await message.reply("❌ Could not understand the audio.")
                        
                except Exception as e:
                    await message.reply(f"❌ Error processing audio: {str(e)}")
    
    await bot.process_commands(message)

async def convert_audio_to_text(audio_data):
    """Convert audio data to text"""
    try:
        # Create a temporary audio source from the data
        audio_source = sr.AudioData(audio_data, 16000, 2)
        text = r.recognize_google(audio_source)
        return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        print(f"Speech recognition error: {e}")
        return None

# Run the bot
# bot.run('YOUR_BOT_TOKEN')