from sys import byteorder
from array import array
from struct import pack

import pyaudio
import wave
import speech_recognition as sr
import time
from datetime import datetime
import os


current_dir = os.getcwd()


def big_function():
    def callback(recognizer, audio):
        # received audio data, now we'll recognize it using Google Speech Recognition
        try:
            # for testing purposes, we're just using the default API keyto use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
            # instead of `r.recognize_google(audio)`
            print("--------" + recognizer.recognize_google(audio, language="uz-UZ"))
            value = recognizer.recognize_google(
                audio, language="uz-UZ")
            print("Recording")
            cheating_time = datetime.now().strftime("%H-%M-%S")
            with open(os.path.join(f"{current_dir}/audios/{cheating_time}.wav"), 'wb') as file1:
                file1.write(audio.get_wav_data())

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    r = sr.Recognizer()
    m = sr.Microphone()
    with m as source:
        # we only need to calibrate once, before we start listening
        r.adjust_for_ambient_noise(source)

    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # do some unrelated computations for 5 seconds
    # we're still listening even though the main thread is doing other things
    for _ in range(50):
        time.sleep(3)

    # calling this function requests that the background listener stop listening
    # stop_listening(wait_for_stop=False)

    # do some more unrelated things
    while True:
        time.sleep(0.1)


big_function()
