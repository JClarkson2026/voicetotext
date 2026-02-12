import speech_recognition as sr
import time
from gtts import gTTS
import pygame
import os

class VoiceToText:
    def __init__(self, device_index):
        self.r = sr.Recognizer()
        self.r.energy_threshold = 300
        self.r.dynamic_energy_threshold = False

        self.mic = sr.Microphone(
            device_index=device_index,
            sample_rate=16000
        )

        # Warm-up (critical)
        with self.mic as source:
            time.sleep(0.5)

    def listen(self):
        try:
            with self.mic as source:
                audio = self.r.listen(
                    source,
                    timeout=3,
                    phrase_time_limit=5
                )
        except sr.WaitTimeoutError:
            return None
        except Exception as e:
            print("Mic error:", e)
            return None

        return self.recognize(audio)

    def recognize(self, audio):
        try:
            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            return None
        except sr.RequestError as e:
            print("API error:", e)
            return None

class TextToVoice:
    def __init__(self, lang='en'):
        self.lang = lang

    def speak(self, text):
        try:
            mytext = text

            language = 'en'

            myobj = gTTS(text=mytext, lang=language, slow=False)

            # Saving the converted audio in a mp3 file named
            # welcome 
            myobj.save("audio.mp3")

            # Initialize the mixer module
            pygame.mixer.init()

            # Load the mp3 file
            pygame.mixer.music.load("audio.mp3")

            # Play the loaded mp3 file
            pygame.mixer.music.play()
        except Exception as e:
            print("TTS error:", e)
