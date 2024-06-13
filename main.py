import requests
import pyttsx3
import pyaudio
import json
from vosk import Model, KaldiRecognizer
from datetime import datetime

engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 0.9)

def speak(text):
    engine.say(text)
    engine.runAndWait()

model = Model(model_name="vosk-model-tts-ru-0.6-multi")
recognizer = KaldiRecognizer(model, 16000)

def listen():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    print("Слушаю...")
    while True:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            text = json.loads(result)['text']
            if text:
                print(f"Распознано: {text}")
                return text
            
def process_command(command):
    if "привет" in command:
        speak("Привет! Чем могу помочь?")
    elif "время" in command:
        now = datetime.now().strftime("%H:%M")
        speak(f"Сейчас {now}")
    elif "погода" in command:
        speak("Пожалуйста, подождите, я получаю информацию о погоде.")
        response = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Санкт-Петербург&appid=7e5035a9ffb9d723b6fdf7b2955e86f7&units=metric&lang=ru")
        weather_data = response.json()
        if weather_data.get('weather'):
            weather = weather_data['weather'][0]['description']
            temp = weather_data['main']['temp']
            speak(f"Сейчас в Санкт-Петербурге {weather}, температура {temp} градусов Цельсия.")
        else:
            speak("Не удалось получить информацию о погоде.")
    elif "новость" in command:
        speak("Пожалуйста, подождите, я получаю последние новости.")
        response = requests.get("https://newsapi.org/v2/top-headlines?country=ru&apiKey=abc83543935d472b99d8f2ea2432912a")
        news_data = response.json()
        if news_data.get('articles'):
            top_article = news_data['articles'][0]
            speak(f"Вот последняя новость: {top_article['title']}")
        else:
            speak("Не удалось получить новости.")
    else:
        speak("Извините, я не понял команду.")

def main():
    speak("Чем могу помочь?")
    while True:
        command = listen()
        process_command(command)

if __name__ == "__main__":
    main()

