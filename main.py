from voiceFunctions import VoiceToText, TextToVoice


PIPEWIRE_INDEX = 10  # <-- replace with actual index

print("Starting voice assistant...")
listener = VoiceToText(device_index=PIPEWIRE_INDEX)
speaker = TextToVoice()

while True:
    command = listener.listen()
    if command:
        print("Command received:", command)
        speaker.speak(command)

        