#!/usr/bin/python3
import scipy.io
from scipy.io import wavfile

from hilbert import *
from sig_gen import *
from window import *

###############################################################################
# constants
###############################################################################
fname = "Onslaught demo.wav"
n = 125

# per FIR compiler rules for hilbert transform length
hilbert_len = int(4 * n + 3)


fs, audio = wavfile.read(fname)
print(f"number of channels = {audio.shape[1]}")
length = audio.shape[0]
print(f"File length (samples): {length}")

# print(f"max L: {audio[:,0].max()}, max r: {audio[:,1].max()}")
# print(f"min L: {audio[:,0].min()}, min r: {audio[:,1].min()}")
print("Generating hilbert transform")

print("FFT spectrum (left channel) 0.5 second, windowed")
offset = int(3 * fs)
length = int(0.5 * fs)
