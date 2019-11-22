import pyaudio
import wave
import numpy as np
from array import array
from sys import byteorder
THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = pyaudio.paInt16
Fs = 96000

def is_silent(data):
    # determines if a chunk of data contains silence or noise
    return max(data) < THRESHOLD

def normalize(data):
    MAXIMUM_VAL = 16384
    mult = float(MAXIMUM)/max(abs(samp) for samp in data)

    r = array('h')
    for samp in data:
        r.append(int(sample*mult))
    return r

def play_and_record():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=Fs, input=True, output=True, frames_per_buffer=CHUNK_SIZE)
    # TODO: Delay a fixed N seconds and asynchronously play the sound

    r = array('h')

    num_silent_chunks = 0
    heard_tone = False

    while (True):
        # data needs to be little endian, signed short
        data =
        array('h', stream.read(CHUNK_SIZE))
        if (byteorder == 'big'):
            data.byteswap()
        r.extend(data)

        silent = is_silent(data)

        if (silent and heard_tone):
            num_silent_chunks += 1
        elif (not silent and not heard_tone):
            # Have now heard a noise / didn't have silence: update state
            heard_tone = True

        if (heard_tone and num_silent_chunks > 30):
            # Have heard enough silence after the tone (~0.33s) to comfortably break
            break

    samp_width = p.get_sample_size(FORMAT)
    stream.stop_stream
    stream.close()
    p.terminate()

    r = normalize(r)            # Normalize audio value
    return sample_width, r      # Return size of 1 sample + all data

def record_to_file(filepath):
    samp_width, data = play_and_record()
    data = pack('<' + ('h'*len(data)), *data)

    wav_file = wave.open(filepath, 'wb')    # write mode
    wav_file.setnchannels(1)                # mono
    wav_file.setsampwidth(samp_width)       # 16 bit
    wav_file.setframerate(Fs)               # 96 kHz
    wav_file.writeframes(data)              # write the data (correct format)
    wav_file.close()                        # the word is writ


if __name__ == '__main__':
    input ("Type YES when you are ready for the first recording:")
    record_to_file('recordings/recording1.wav')

    input ("Type YES when you are ready for the second recording:")
    record_to_file('recordings/recording2.wav')

    input ("Type YES when you are ready for the third recording:")
    record_to_file('recordings/recording3.wav')

    print ("Done - everytihng written!")
