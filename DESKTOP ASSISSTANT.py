import pyttsx3
import datetime
import pyaudio
import speech_recognition as sr
import wikipedia
import os
import webbrowser
import smtplib  # to send emais
import pyjokes
import psutil   # keeps a track of various resources utilization in the system like CPU, memory, disks
import pyautogui    #simulate mouse cursor moves and clicks as well as keyboard button presses
import random
import requests
from bs4 import BeautifulSoup
import subprocess
import tkinter
from pprint import pprint


Admin = "Ash"
print("Initializing Work-Buddy....")
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


# Main function for the Assistant to speak
def speak(audio):
    engine.say(audio)
    engine.runAndWait()        # for making voice audiable

def change_voice():
    eng = pyttsx3.init()
    voice = eng.getProperty('voices')
    eng.setProperty('voice', voice[1].id)
    eng.say("Hello, How can we help you ? ")
    eng.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")

        r.pause_threshold = 0.7
        audio = r.listen(source)

    try:
        print("Recognizing")
        query = r.recognize_google(audio, language='en-in')
        print(f"{Admin} said: {query}\n")

    except Exception as e:
        print(e)
        speak("Unable to recgnize...Can you say that again please....")
        return "None"

    return query

# extracting time
def time():
    Time = datetime.datetime.now().strftime("%H:%M:%S %p")
    speak("The Present Time is:  ")
    speak(Time)

def Date():
    d = datetime.datetime.now().strftime("%d")
    m = datetime.datetime.now().strftime("%B")
    y = datetime.datetime.now().strftime("%Y")
    da = datetime.datetime.now().strftime("%A")
    speak("Today's Date is "+d+"th "+m+" "+y)
    speak("It's "+da+" Today")

def wish_user():
    speak("Welcome Back!")
    time()
    Date()

    hr = datetime.datetime.now().hour
    if(hr>=0 and hr<12):
        speak("Good Morning" + Admin)
    elif(hr>=12 and hr<15):
        speak("Good Afternoon" + Admin)
    elif(hr>=15 and hr<24):
        speak("Good Evening" + Admin)
    else:
        speak("Good Night" + Admin)
    speak("Work Buddy at ur service, How can I help you?")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()       #to inform the email server that the email client wants to upgrade from an insecure connection to a secure one using TLS or SSL
    server.login('ashineekesanam@gmail.com', "Ashmaanu#20")
    server.sendmail("ashineekesanam@gmail.com", to, content)
    server.close()


def cpu():
    usage = str(psutil.cpu_percent())
    speak('CPU is at '+usage)

    battery = psutil.sensors_battery()
    speak("Battery left: ")
    speak(battery.percent)

    speak('RAM memory % used:', psutil.virtual_memory()[2])
    speak("RAM memory used in GB: ", psutil.virtual_memory()[3]/1000000000)

def screenshot():
    img = pyautogui.screenshot()
    img.save('D:/SCREENSHOTS/ss1.png')

def joke():
    speak(pyjokes.get_joke())

def about_me():
    speak("You are " + Admin)

def how_are_you():
    speak("I'm good, Thank You. How can I help you?")


def getNews():
    try:
        response = requests.get('https://www.bbc.com/news')

        b4soup = BeautifulSoup(response.text, 'html.parser')
        headLines = b4soup.find('body').find_all('h3')
        unwantedLines = ['BBC World News TV', 'BBC World Service Radio',
                         'News daily newsletter', 'Mobile app', 'Get in touch']
        for x in list(dict.fromkeys(headLines)):
            if x.text.strip() not in unwantedLines:
                speak(x.text.strip())
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    change_voice()

    wish_user()

    while True:
        query = takeCommand().lower()

        if 'time' in query:
            time()

        elif 'date' in query:
            Date()

        elif 'who am i' in query:
            about_me()

        elif 'how are you' in query:
            how_are_you()

        elif 'wikipedia' in query.lower():
            speak("opening wikipedia...")
            time.sleep(3)
            speak("What should I search for?")
            question = takeCommand().lower()
            answer = wikipedia.search(question)
            result = wikipedia.summary(answer, sentences=3)
            speak('According to wikipedia...')
            print(result)
            speak(result)

        elif 'search in google' in query.lower():
            speak('What should I search?')
            chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe %s"
            search = takeCommand().lower()
            speak("Opening Google...")
            webbrowser.get(chrome_path).open_new_tab(search+'.com')

        elif 'search youtube' in query:
            speak('What should I Search?')
            search_term = takeCommand().lower()
            speak("Opening YOUTUBE!")
            webbrowser.open('https://www.youtube.com/results?search_query=' + search_term)

        elif 'weather details' in query:
            speak("Which city's details would u like to know? ")
            city_name = takeCommand().lower()
            speak("getting weather Update for " + city_name)
            api_key = "bac50bdeec11084ecaa9bb78d6d60ccb"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name

            req = requests.get(complete_url)
            data = req.json()

            temp = data['main']['temp'],
            wind_speed = data['wind']['speed'],
            pressure = data['humidity'],
            latitude = data['coord']['lat'],
            longitude = data['coord']['lon'],
            description = data['weather'][0]['description']

            speak('Temperature is at: {} degree celcius'.format(temp))
            speak('Wind Speed is at: {} Micro Seconds'.format(wind_speed))
            speak('Pressure is : {}'.format(pressure))
            speak('Latitude is : {}'.format(latitude))
            speak('Longitude is : {}'.format(longitude))
            speak('Clouds Status are : {}'.format(description))


        elif 'open google' in query:
            speak('What should I Search?')
            search_term = takeCommand().lower()
            speak('Searching...')
            url = 'google.com'
            chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe %s"
            webbrowser.open('https://www.google.com/search?q=' + search_term)

        elif 'send email' in query.lower():
            try:
                speak('Who is the receiver? ')
                receiver = input("Enter Receiver's email ID: ")
                to = receiver
                speak('What is the content of the email ? ')
                content = takeCommand()
                sendEmail(to, content)
                speak("Email sent successfully..")
            except Exception as e:
                print(e)
                speak('Unable to send email... Will rectify it soon..')

        elif 'open word' in query:
            speak('Opening MS Word....')
            ms_word = r'C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE'
            os.startfile(ms_word)

        elif 'open downloads' in query:
            speak('Opening Downloads....')
            downloads = r'C:\Users\Dell\Downloads'
            os.startfile(downloads)

        elif 'write a note' in query:
            speak("What notes should I take down ?")
            notes = takeCommand()
            file = open('note1.txt', 'w')
            speak("Should I include Date and Time?")
            ans = takeCommand()
            if 'yes' in ans or 'sure' in ans:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                file.write(strTime)
                file.write(':-')
                file.write(notes)
                speak("Done taking Notes....")
            else:
                file.write(notes)

        elif 'show notes' in query:
            speak('showing the notes: ')
            file = open('note1.txt', 'r')
            print(file.read())
            speak(file.read())

        elif 'screenshot' in query:
            screenshot()

        elif 'change voice' in query:
            change_voice()

        elif 'cpu' in query:
            cpu()

        elif 'joke' in query:
            joke()

        elif 'news' in query:
            getNews()

        elif 'play music' in query:
            song_directory = "D:\MUSIC"
            music = os.listdir(song_directory)
            speak('Which song would u like to hear? ')
            speak("select a number: ")
            ans = takeCommand().lower()
            while('number' not in answer and answer != 'random' and answer!= 'you choose'):
                speak('unable to hear you. Can u come again..')
                ans = takeCommand().lower()
            if 'number' in answer:
                num = int(ans.replace("number", ""))
            elif 'random' or 'you choose' in answer:
                num = random.randint(1,3)
            os.startfile(os.path.join(song_directory, music[num]))

        elif 'who are you' in query:
            speak("I am work buddy, the smart desktop assistant of {Admin} developed to help the Admin with the work")

        elif 'shutdown system' in query:
            speak("Your system is on its way to shut down... starting your command")
            subprocess.call('shutdown / p /f')

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])

        elif 'exit' in query:
            speak("Thanks for giving me your time")
            exit()





