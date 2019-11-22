import numpy as np
import matplotlib.pyplot as plt

def get_time_delay(x, y, Fs):
    """x is recorded signal - bytes
    y is input signal - bytes
    Fs is sampling rate
    """
    # Type check
    assert(isinstance(x, bytes))
    assert(isinstance(y, bytes))

    # Convert little-endian bytes to list
    x_values = np.array([ int.from_bytes(bytes([x[i], x[i+1]]), 'little', signed=True) for i in range(0, len(x), 2) ])
    y_values = np.array([ int.from_bytes(bytes([y[i], y[i+1]]), 'little', signed=True) for i in range(0, len(y), 2) ])

    # Now: Need to correlate the recording with the expected tone to find time delay

    # Figure out length to adjust to
    x_len = len(x_values)
    print("x (recording) lasts", x_len/Fs, "seconds")
    y_len = len(y_values)
    print ("y (tone) lasts", y_len/Fs, "seconds")
    max_len = max(x_len*2, y_len*2)

    # Zero pad both signals
    xz = np.concatenate((x_values, np.zeros(max_len-x_len)))
    yz = np.concatenate((y_values, np.zeros(max_len-y_len)))

    # Correlate:
    #   - Take fft of each
    #   - Complex conj. fft of y
    #   - Multiply together
    #   - Inverse FFT
    correlation = np.fft.irfft( np.fft.rfft(xz) * np.conj( np.fft.rfft(yz) ) )
    assert (len(xz)==max_len)
    assert (len(correlation)==max_len)
    #print(correlation)
    horiz = np.arange(1, len(correlation)+1) / Fs
    #plt.plot(horiz, xz)
    #plt.plot(horiz, yz)
    #plt.xlabel("time [s]")
    #plt.ylabel("amplitude (sound)")
    #plt.title("sound signals")
    plt.plot(horiz, correlation)
    plt.xlabel("time delay [s]")
    plt.ylabel("correlation")
    plt.title("correlation of recording with input tone")
    plt.show()

    # Detect the peak of the correlation
    delay = np.argmax(correlation)

    # Time delay (s) - sample delay / sampling rate
    return delay / Fs

if __name__ == "__main__":
    inputs = [[1, 2, 3], [1, 0, 1], [0, 1, 0]]
    recordings = [
            [[0, 0, 1, 2, 3, 0, 0],
            [1, 2, 3, 0, 0],
            [0, 0, 1, 2, 4, 0, 0, 0]],

            [[0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0],
            [0, 0, 1, 0, 1],
            [1, 0, 1]],

            [[0, 0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 1]]

        ]

    for i in range(len(inputs)):
        for j in range(len(inputs[i])):
            print("\n\n")
            delay = get_time_delay(np.array(recordings[i][j]), np.array(inputs[i]), 1)
            print("Correlating recording", recordings[i][j], "with input", inputs[i], "Fs = 1: Delay == ", delay)
