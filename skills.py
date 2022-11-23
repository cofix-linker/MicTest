# import pyttsx3

# engine = pyttsx3.init()
# voices = engine.getProperty('voices')
# engine.setProperty('voice', 'ru')
# engine.setProperty('rate', 180)
# for voice in voices:
#     if voice.name == "Irina":
#         engine.setProperty("voice", voice.id)
#
# def speaker(text):
#     engine.say(text)
#     engine.runAndWait()

import os

def speaker(text):
    os.system(f"echo «{text}» | RHVoice-test -p anna")
