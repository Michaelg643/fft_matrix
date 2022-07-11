#!/usr/bin/python3
from scipy.io import wavfile
import scipy.io

from hilbert import *
from window import *
from sig_gen import *

################################################################################
## constants
################################################################################
fname = 'Onslaught demo.wav'
n = 125
hilbert_len = int(4*n+3) #per FIR compiler rules for hilbert transform length


fs, audio = wavfile.read(fname)
print(f"number of channels = {audio.shape[1]}")
length = audio.shape
print(f"File length (samples): {length}")

#print(f"max L: {audio[:,0].max()}, max r: {audio[:,1].max()}")
#print(f"min L: {audio[:,0].min()}, min r: {audio[:,1].min()}")
print('Generating hilbert transform')

print('real-cx FFT spectrum (left channel) 0.5 second, windowed')
offset = int(3*fs)
length = int(0.5*fs)

