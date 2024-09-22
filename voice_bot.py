import speech_recognition as sr
from gtts import gTTS
import os
import requests

def get_audio_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"User said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Could not request results; check your network connection.")
            return None

def speak_text(text):
    tts = gTTS(text=text, lang='en')
    tts.save('response.mp3')
    os.system('start response.mp3')

def send_to_rasa(user_input):
    # Replace 'http://localhost:5005/webhooks/rest/webhook' with your Rasa server URL
    rasa_url = 'http://localhost:5005/webhooks/rest/webhook'
    response = requests.post(rasa_url, json={"sender": "user", "message": user_input})
    if response.status_code == 200:
        messages = response.json()
        if messages:
            return messages[0].get('text', '')
    return "Sorry, I didn't get that."

def main():
    while True:
        user_input = get_audio_input()
        if user_input is not None:
            bot_response = send_to_rasa(user_input)
            print(f"Bot says: {bot_response}")
            speak_text(bot_response)

if __name__ == "__main__":
    main()