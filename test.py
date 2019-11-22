import numpy as np
from timedelay import get_time_delay
import wave

tone = wave.open("tone.wav")
recording = wave.open("recordings_test/myhal_stairwell_laptop.wav")

print (recording.getnchannels(), tone.getnchannels())
print (recording.getframerate(), tone.getframerate())
print (recording.getnframes(), tone.getnframes())
print (recording.getnframes() / recording.getframerate(), tone.getnframes() / tone.getframerate())
delay = get_time_delay(recording.readframes(recording.getnframes()), tone.readframes(tone.getnframes()), recording.getframerate())


print ("Time delay between recording and tone (Fs = 96000):", delay)
