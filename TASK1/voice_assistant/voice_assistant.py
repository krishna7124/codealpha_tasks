import pyttsx3
import speech_recognition as sr
import datetime
import webbrowser
import wikipedia
import os
import random

try:
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

    def speak(audio):
        engine.say(audio)
        engine.runAndWait()

    def greet():
        hour = datetime.datetime.now().hour
        if 0 <= hour < 12:
            speak(f"Good Morning!")
        elif 12 <= hour < 18:
            speak(f"Good Afternoon!")
        else:
            speak(f"Good Evening!")
        speak("Welcome, I am your personal assistant, Viraj.")

    def VoiceCommand():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(e)
            print("Unable to Recognize your voice.")
            return "None"
        return query

    def tell_joke():
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Parallel lines have so much in common. It's a shame they'll never meet.",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why did the scarecrow win an award? Because he was outstanding in his field!"
        ]
        joke = random.choice(jokes)
        speak(joke)

    if __name__ == '__main__':

        greet()
        while True:
            work = VoiceCommand().lower()
            if 'hello' in work:
                speak('Hi, how can I help you?')

            elif 'open notepad' in work:
                speak('Opening Notepad for you....')
                path = ("c:\\windows\\system32\\notepad.exe")
                os.startfile(path)
            elif 'close notepad' in work:
                speak('Closing Notepad, please wait....')
                os.system('taskkill /f /im notepad.exe')

            elif 'open youtube' in work:
                speak("Opening YouTube. What would you like to search?")
                query = VoiceCommand().lower()
                if query != 'none':
                    url = f"https://www.youtube.com/results?search_query={query}"
                    webbrowser.open(url)

            elif 'open google' in work:
                speak("Opening Google. What would you like to search?")
                query = VoiceCommand().lower()
                if query != 'none':
                    url = f"https://www.google.com/search?q={query}"
                    webbrowser.open(url)

            elif 'play music' in work:
                speak('Opening music player....')
                path = (
                    "C:\\Program Files (x86)\\Windows Media Player\\wmplayer.exe")
                os.startfile(path)

            elif 'open mail' in work:
                speak("Opening Mail.")
                webbrowser.open("https://mail.google.com/mail/u/0/#inbox")

            elif 'open whatsapp' in work:
                speak("Opening WhatsApp for you.")
                webbrowser.open("https://web.whatsapp.com/")

            elif 'tell me a joke' in work:
                tell_joke()

            elif 'exit' in work:
                speak("Thanks for giving me your time. Have a nice day!")
                exit()

except KeyboardInterrupt:
    print("Keyboard Interrupt detected. Exiting...")

except BaseException as ex:
    print(f"Error occurred: {ex}")

finally:
    print("Thank you. Goodbye, have a nice day!")
