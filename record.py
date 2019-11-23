import numpy as np
from array import array
import sounddevice as sd
import soundfile as sf
import queue
import datetime

Fs = 96000

def normalize(data):
    MAXIMUM_VAL = 16384
    mult = float(MAXIMUM_VAL)/max(abs(samp) for samp in data)

    r = array('h')
    for samp in data:
        r.append(int(sample*mult))
    return r

q = queue.Queue()
def play_and_record(filename):
    def audio_callback(data, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        q.put(data[:, [0]])
    try:
        with sf.SoundFile(filename, mode='x', samplerate=Fs, channels=1) as file:
            tone_data, tone_Fs = sf.read("tone.wav")
            print("RECORDING")
            start = datetime.datetime.now()
            with sd.InputStream(channels=1, samplerate=Fs, callback=audio_callback):
                sd.play(tone_data, tone_Fs)
                end = datetime.datetime.now()
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print("DONE RECORDING - INTRINSIC DELAY WAS:", (end - start).total_seconds(), "s")


if __name__ == '__main__':
    input ("Type YES when you are ready for the first recording:")
    play_and_record('recordings/recording1.wav')

    input ("Type YES when you are ready for the second recording:")
    play_and_record('recordings/recording2.wav')

    input ("Type YES when you are ready for the third recording:")
    play_and_record('recordings/recording3.wav')

    print ("Done - everytihng written!")
