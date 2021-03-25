import gtts
from playsound import playsound
# https://www.thepythoncode.com/article/convert-text-to-speech-in-python

# make request to google to get synthesis
tts = gtts.gTTS("Písmeno Bé .  Jako Autobus, Ananas, Auto, Anténa, Andílek", lang="cs")
# save the audio file
tts.save("speech.mp3")
# play the audio file
#playsound("speech.mp3")

tts = gtts.gTTS("I have watched you correct my work. I guess I have misunderstood the assignment in some cases.", lang="en")
tts.save("druha.mp3")
playsound("druha.mp3")
