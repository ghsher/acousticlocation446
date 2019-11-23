import wave
import numpy as np
from array import array
from sys import byteorder
import sounddevice as sd
import soundfile as sf
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import queue
import sys

THRESHOLD = 500
CHUNK_SIZE = 1024
FORMAT = 0 #pyaudio.paInt16
Fs = 96000

def is_silent(data):
    # determines if a chunk of data contains silence or noise
    return max(data) < THRESHOLD

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
            with sd.InputStream(channels=1, samplerate=Fs, callback=audio_callback):
                print("RECORDING")
                print("PLAYING")
                tone_data, tone_Fs = sf.read("tone.wav")
                sd.play(tone_data, tone_Fs)
                import time
                time.sleep(0.1)
                print("DONE PLAYING")
                while True:
                    file.write(q.get())
    except KeyboardInterrupt:
        print("DONE RECORDING")
"""
plotdata = 0
///
    def update_plot(frame):
        global plotdata
        while True:
            try:
                data = q.get_nowait()
            except queue.Empty:
                break
            shift = len(data)
            plotdata = np.roll(plotdata, -shift, axis=0)
            plotdata[-shift:, :] = data
        for column, line in enumerate(lines):
            line.set_ydata(plotdata[:, column])
        return lines
    /////
        global plotdata
        length = int(200 * Fs / (1000))
        plotdata = np.zeros((length, len(channels)))
        fig, ax = plt.subplots()
        lines = ax.plot(plotdata)
        if len(channels) > 1:
            ax.legend(['channel {}'.format(c) for c in channels], loc='lower left', ncol = len(channels))
        ax.axis((0, len(plotdata), -1, 1))
        ax.set_yticks([0])
        ax.yaxis.grid(True)
        ax.tick_params(bottom=False, top=False, labelbottom=False, right=False, left=False, labelleft=False)
        fig.tight_layout(pad=0)

        ani = FuncAnimation(fig, update_plot, interval=30, blit=True)
"""
#    with wave.open(filename, 'wb') as wav_file:
 #       wav_file.setnchannels(1)                # mono
   #     wav_file.setsampwidth(2)       # 16 bit
  #      wav_file.setframerate(Fs)               # 96 kHz
    #    audiodata = array('h')
     #   with stream:
      #      plt.show()
       # while (not q.empty()):
        #    a = q.get()
         #   print(a, "END")
          #  audiodata.extend()
#        print(audiodata)
#
 #       data = normalize(audiodata)
  #      data = pack('<' + ('h'*len(data)), *data)
   #     wav_file.writeframes(data)              # write the data (correct format)
    #    wav_file.close()                        # the word is writ

def play_and_record_old():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=1, rate=Fs, input=True, output=True, frames_per_buffer=CHUNK_SIZE)
    # TODO: Delay a fixed N seconds and asynchronously play the sound

    r = array('h')

    num_silent_chunks = 0
    heard_tone = False

    while (True):
        # data needs to be little endian, signed short
        data = array('h', stream.read(CHUNK_SIZE))
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
    play_and_record('recordings/recording1.wav')

    input ("Type YES when you are ready for the second recording:")
    play_and_record('recordings/recording2.wav')

    input ("Type YES when you are ready for the third recording:")
    play_and_record('recordings/recording3.wav')

    print ("Done - everytihng written!")
