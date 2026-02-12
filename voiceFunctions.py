
---

# 🧩 Commented Module (`voiceFunctions.py`)

```python
import speech_recognition as sr
import time
from gtts import gTTS
import pygame
import os


class VoiceToText:
    """
    Handles microphone input and converts speech to text
    using Google Speech Recognition.
    """

    def __init__(self, device_index):
        # Initialize the speech recognizer
        self.r = sr.Recognizer()

        # Fixed energy threshold for more predictable behavior
        self.r.energy_threshold = 300
        self.r.dynamic_energy_threshold = False

        # Configure microphone
        self.mic = sr.Microphone(
            device_index=device_index,
            sample_rate=16000  # Optimal sample rate for speech recognition
        )

        # Warm-up the microphone (prevents first-read ALSA/PortAudio issues)
        with self.mic as source:
            time.sleep(0.5)

    def listen(self):
        """
        Listens for a single spoken phrase and returns
        recognized text or None.
        """
        try:
            with self.mic as source:
                audio = self.r.listen(
                    source,
                    timeout=3,           # Max time waiting for speech
                    phrase_time_limit=5  # Max length of a spoken phrase
                )
        except sr.WaitTimeoutError:
            # No speech detected
            return None
        except Exception as e:
            # Any microphone / PortAudio error
            print("Mic error:", e)
            return None

        return self.recognize(audio)

    def recognize(self, audio):
        """
        Converts recorded audio to text using Google Speech API.
        """
        try:
            return self.r.recognize_google(audio)
        except sr.UnknownValueError:
            # Speech was unintelligible
            return None
        except sr.RequestError as e:
            # API or network error
            print("API error:", e)
            return None


class TextToVoice:
    """
    Converts text to speech and plays it back using gTTS and pygame.
    """

    def __init__(self, lang='en'):
        self.lang = lang

    def speak(self, text):
        """
        Converts text to speech, saves it as an MP3,
        and plays it using pygame.
        """
        try:
            # Generate speech audio using Google Text-to-Speech
            tts = gTTS(text=text, lang=self.lang, slow=False)

            # Save audio to file
            audio_file = "audio.mp3"
            tts.save(audio_file)

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

        except Exception as e:
            print("TTS error:", e)
