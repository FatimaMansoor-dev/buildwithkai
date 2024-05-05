import pyttsx3
import speech_recognition 
import requests 
from bs4 import BeautifulSoup

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        print("Listening.....")
        r.pause_threshold = 1
        r.energy_threshold = 300
        audio = r.listen(source,0,4)

    try:
        print("Understanding..")
        query  = r.recognize_google(audio,language='en-in')
        print(f"You Said: {query}\n")
    except Exception as e:
        print("Say that again")
        return "None"
    return query

if __name__ == "__main__":
    while True:
        query = takeCommand().lower()
        if "wake up" in query:
            speak('Yes sir at your service')

            while True:
                query = takeCommand().lower()
                if "go to sleep" in query:
                    speak("Ok sir , You can me call anytime")
                    url = 'http://localhost:5000/'  # Change URL if needed
                    requests.get(url)
                    break 
                ## searching
                elif ('search' in query)  and ('google' in query):
                    from search import search_google
                    search_google(query)
                elif (('search' in query) or('play' in query))  and ('youtube' in query):
                    from search import search_yt
                    search_yt(query)

                ## temperature and weather
                elif 'what is the temperature' in query:
                        # search = 'temperature in karachi'
                        # place = 'karachi'
                        if 'in' in query:
                            place = query.split('in')[1]
                            search = 'temperature in '+place
                        url = 'https://www.google.com/search?q=' + search
                        page = requests.get(url)
                        soup = BeautifulSoup(page.text, 'html.parser')
                        temp = soup.findAll('div', {'class': 'BNeawe iBp4i AP7Wnd'})[1].text
                        speak(f'The current temperature in {place} is {temp}.')

                elif 'what is the weather' in query or ('tell' in query and 'weather' in query):
                    # search = 'weather in karachi'
                    # place = 'karachi'
                    if 'in' in query:
                        place = query.split('in')[1]
                        search = 'weather in '+place
                    url = 'https://www.google.com/search?q=' + search
                    page = requests.get(url)
                    soup = BeautifulSoup(page.text, 'html.parser')
                    weath = soup.find('div', {'class': 'BNeawe tAd8D AP7Wnd'}).text
                    speak(f'The current weather in {place} on {weath}.')