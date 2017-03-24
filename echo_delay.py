
import sys
import wave
import numpy as np
from gcc_phat import gcc_phat


if len(sys.argv) != 3:
    print('Usage: {} near.wav far.wav'.format(sys.argv[0]))
    sys.exit(1)


near = wave.open(sys.argv[1], 'rb')
far = wave.open(sys.argv[2], 'rb')
rate = near.getframerate()

N = rate

window = np.hanning(N)

while True:
    sig = near.readframes(N)
    if len(sig) != 2 * N:
        break

    ref = far.readframes(N)
    sig_buf = np.fromstring(sig, dtype='int16')
    ref_buf = np.fromstring(ref, dtype='int16')
    tau, _ = gcc_phat(sig_buf * window, ref_buf * window, fs=rate, max_tau=1)
    # tau, _ = gcc_phat(sig_buf, ref_buf, fs=rate, max_tau=1)
    print(tau * 1000)

