
import speech_recognition as sr
import pyttsx3

r = sr.Recognizer()
engine = pyttsx3.init()

def record_text():
    while(1):
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                text = r.recognize_google(audio)
                print(f"You said: {text}")

                return text
            
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio. Please try again.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return

def output_text(text):
    f = open("output.txt", "a")
    f.write(text)
    f.write("\n")
    f.close()
    return

while True:
    text = record_text()
    output_text(text)

    print("Recorded and outputted text.")