import numpy as np
from timedelay import get_time_delay
import wave

tone = wave.open("tone.wav")
tone_channels = tone.getnchannels()
tone_framerate = tone.getframerate()
tone_frames = tone.getnframes()
tone_data = tone.readframes(tone_frames)
for i in range(3):
    recording = wave.open("recordings/recording" + str(i+1) + ".wav")

    print (recording.getnchannels(), tone_channels)
    print (recording.getframerate(), tone_framerate)
    print (recording.getnframes(), tone_frames)
    print (recording.getnframes() / recording.getframerate(), tone_frames / tone_framerate)
    delay = get_time_delay(recording.readframes(recording.getnframes()), tone_data, recording.getframerate())


    print ("Time delay between recording", i+1, "and tone (Fs = 96000):", delay)
