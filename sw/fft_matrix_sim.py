#!/usr/bin/python3
"""Simulation of what the FFT Matrix should be doing."""

import numpy as np
import scipy.io
from scipy.io import wavfile

import hilbert
import sig_gen
import window

###############################################################################
# simulation parameters
###############################################################################
fname = "Onslaught demo.wav"
nfft = 16384
overlap = 1024  # samples
nbits = 16
audio_ch = 0
fc = 1000  # how much to shift the audio by in the frequency domain
npts = 64
min_freq = fc + 20
max_freq = fc + 20e3

b = window.approximate_b(60)
print("Generating window")
fp_win, win = window.fixed_point_kaiser2(nfft, b, nbits)

print("Reading Audio")
fs, audio = wavfile.read(fname)
print(f"number of channels = {audio.shape[1]}")
length = audio.shape[0]
print(f"File length (samples): {length}")

n = np.arange(length)
complex_mult = np.exp(1j * 2 * np.pi * fc / fs * n)
sample_counter = 0  # Keeps track of where we're at in the audio file
shifted_audio = audio[:, audio_ch] * complex_mult

while sample_counter < length:
    print(f"Start index: {sample_counter}")
    print(f"Stop index: {sample_counter + nfft - 1}")
    current_slice = shifted_audio[sample_counter : sample_counter + nfft]
    windowed_audio = current_slice * win
    sp, freq = sig_gen.gen_full_spectrum(windowed_audio, nfft, fs)

    freq_dict_array = sig_gen.determine_bins(freq, npts, min_freq, max_freq)
    sp_norm, freq_norm = sig_gen.freq_int(sp, freq, freq_dict_array)
    sig_gen.plot_spectrum(fs, sp, freq, sp_norm, freq_norm)
    sample_counter = sample_counter + nfft - overlap
