from flask import Flask, render_template, request, jsonify
import os
import time
import pyaudio
import speech_recognition as sr
import playsound
from gtts import gTTS
import openai

app = Flask(__name__)

# Initialize a counter variable
counter = 0
api_key = "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"
lang = 'en'
openai.api_key = api_key
guy = ""
    
@app.route('/')
def index():
    return render_template('/idex.html', text="Click here to speak")

@app.route('/listen', methods=['POST'])
def listen():
    def get_adio():
        r = sr.Recognizer()
        with sr.Microphone(device_index=1) as source:
            audio = r.listen(source)
            said = ""

            try:
                said = r.recognize_google(audio)
                print(said)
                global guy
                guy = said

                if "ultron" in said.lower():
                    words = said.split()
                    new_string = ' '.join(words[1:])
                    completion = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": said}]
                    )
                    text = completion.choices[0].message["content"]
                    print(completion.choices[0].message)
                    speech = gTTS(text=text, lang=lang, slow=False, tld="com.au")
                    speech.save("welcome2.mp3")
                    playsound.playsound("welcome2.mp3")
                    os.remove("welcome2.mp3")
            except Exception as e:
                return "Sorry! I couldn't hear anything. Could you repeat please?"
        return said

    return render_template('/idex.html', text=get_adio())

if __name__ == '__main__':
    app.run(debug=True)
