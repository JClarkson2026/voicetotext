# Voice Functions Module
Voice recognition and text-to-speech utilities

## Requirements
- Python 3.9+
- Python packages:
  ```bash
  pip install SpeechRecognition gtts pygame pyaudio
  ```

## Usage

### Setup
```python
import voiceFunctions as VF

# Initialize voice-to-text with microphone device index
voice_input = VF.VoiceToText(device_index=0)

# Initialize text-to-voice with language
voice_output = VF.TextToVoice(lang='en')
```

---

### VoiceToText
Handles microphone input and converts speech to text using Google Speech Recognition

#### Calling function
```python
voice_input = VF.VoiceToText(device_index=0)
```

Parameters:
- `device_index` (int): Microphone device index (use 0 for default microphone)

Configuration:
- Energy threshold: 300 (fixed)
- Dynamic energy threshold: Disabled
- Sample rate: 16,000 Hz (optimal for speech recognition)
- Includes 0.5 second warm-up period to prevent ALSA/PortAudio initialization issues

#### listen
```python
text = voice_input.listen()
```
Listens for a single spoken phrase and returns recognized text

Parameters:
- No arguments

Outputs:
- Returns recognized text as string if speech detected and understood
- Returns `None` if no speech detected (timeout after 3 seconds)
- Returns `None` if speech is unintelligible
- Returns `None` on microphone or API errors (prints error message)

Configuration:
- Timeout: 3 seconds (maximum wait time for speech to begin)
- Phrase time limit: 5 seconds (maximum length of spoken phrase)

#### recognize
```python
text = voice_input.recognize(audio)
```
Converts recorded audio to text using Google Speech API

Parameters:
- `audio` (AudioData): Audio data from speech_recognition library

Outputs:
- Returns recognized text as string on success
- Returns `None` if speech is unintelligible
- Returns `None` on API or network errors (prints error message)

---

### TextToVoice
Converts text to speech and plays it back using gTTS and pygame

#### Calling function
```python
voice_output = VF.TextToVoice(lang='en')
```

Parameters:
- `lang` (str, optional): Language code for speech synthesis (default: 'en')
  - Examples: 'en' (English), 'es' (Spanish), 'fr' (French), 'de' (German)

#### speak
```python
voice_output.speak("Hello, how can I help you?")
```
Converts text to speech, saves it as an MP3, and plays it using pygame

Parameters:
- `text` (str): Text to convert to speech

Outputs:
- Generates and plays audio file
- Creates temporary file `audio.mp3` in current directory
- Prints error message on failure
- No return value

---

## Example Usage

```python
import voiceFunctions as VF

# Initialize voice input and output
voice_input = VF.VoiceToText(device_index=0)
voice_output = VF.TextToVoice(lang='en')

# Greet user
voice_output.speak("Hello! Please say something.")

# Listen for user input
user_speech = voice_input.listen()

if user_speech:
    print(f"You said: {user_speech}")
    voice_output.speak(f"You said: {user_speech}")
else:
    print("No speech detected or couldn't understand.")
    voice_output.speak("Sorry, I didn't catch that.")

# Continuous listening loop
print("Listening continuously. Say 'stop' to exit.")
while True:
    text = voice_input.listen()
    
    if text:
        print(f"Heard: {text}")
        
        if "stop" in text.lower():
            voice_output.speak("Goodbye!")
            break
        else:
            voice_output.speak(f"You said: {text}")
    else:
        print("Listening...")
```

---

## Notes

- **Internet connection required**: Both speech recognition and text-to-speech use Google's cloud services
- **Microphone permissions**: Ensure your application has microphone access permissions
- **Device index**: Use `sr.Microphone.list_microphone_names()` to find available microphone device indices
- **Audio file cleanup**: The `audio.mp3` file is created in the current directory and not automatically deleted
- **Energy threshold**: Fixed at 300 to provide consistent behavior across different environments
- **Timeout behavior**: The `listen()` method will wait up to 3 seconds for speech to begin, then up to 5 seconds for the phrase to complete
- **Error handling**: All methods include error handling and print descriptive error messages
- **Pygame mixer**: Audio playback uses pygame's mixer module, which must be initialized for each playback

---

## Troubleshooting

### Common Issues

**Microphone not detected:**
```python
import speech_recognition as sr
print(sr.Microphone.list_microphone_names())
```
Use the index of your desired microphone from this list.

**ALSA/PortAudio warnings on Linux:**
- These are typically harmless and suppressed by the 0.5 second warm-up period
- If persistent, consider installing `python3-pyaudio` from your system package manager

**Speech recognition returns None:**
- Check internet connection (Google Speech API requires network access)
- Ensure microphone is not muted
- Try speaking louder or closer to the microphone
- Check ambient noise levels (energy threshold is set to 300)

**TTS playback issues:**
- Ensure pygame is properly installed: `pip install pygame`
- Check system audio output is working
- Verify `audio.mp3` file is being created in the current directory