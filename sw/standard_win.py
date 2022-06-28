#!/usr/bin/python3

from kaiser import *
import sig_gen as sg

sll = 80 # db
M = 201 # window length
nbits = 16 # precision of window
nfft = 16384
fs = 2

b = approximate_b(sll)
win = fixed_point_kaiser(M, b, nbits)

sp, freq = sg.gen_full_spectrum(win, nfft, fs)
sp_r, freq_r = sg.gen_full_spectrum(np.round(win), nfft, fs)
sg.plot_window_spectrum(sp, freq, sp_r, freq_r)
sg.plot_sig(win, fs)
