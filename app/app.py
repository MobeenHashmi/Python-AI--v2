from flask import Flask, render_template, request
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib

app = Flask(__name__)

dict_emails = {"a": "osama@demonscombat.com", "b": "mobeenhasan.hashmi@gmail.com",
               "send email to f": "faherhasan@gmail.com", "send email to": "shahzaibquershi@gmail.com",
               "send to": "sshashmi23@gmail.com"}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def send_email(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('syedmobeen08@gmail.com', 'sdr7hr08@A')
    server.sendmail('syedmobeen08@gmail.com', to, content)
    server.close()


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wish_me():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")

    elif 12 <= hour < 18:
        speak("Good Afternoon!")

    else:
        speak("Good Evening!")

    speak("I am Mobeen Assistant, how may I assist you  say something")


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        speak(f"User said: {query}\n")

    except Exception as e:
        print("Say that again please...")
        return "None"
    return query


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process_query', methods=['POST'])
def process_query():
    query = request.form['query'].lower()

    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=1)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'send email' in query:
        try:
            speak("To whom")
            asking_email = take_command()
            mail = dict_emails[asking_email]
            to = mail
            speak("Please tell content of email or what should I say")
            content = take_command()
            send_email(to, content)
            speak("Email has been sent successfully")
        except Exception as e:
            print(e)
            speak("Sorry can not send the email")

    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com/")

    elif 'open google' in query:
        webbrowser.open("https://www.google.com/")

    elif 'open stackoverflow' in query:
        webbrowser.open("https://stackoverflow.com/")

    elif 'time please' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"Respected person, the time is {str_time}")
        print(str_time)
    elif 'who am i' in query:
        speak("Mobeen")

    return render_template('index.html', query_result=query)


if __name__ == '__main__':
    wish_me()
    app.run(debug=True)
