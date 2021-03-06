#!/usr/bin/python3

from window import *
import sig_gen as sg

sll = 80 # db
M = 255 # window length
nbits = 16 # precision of window
nfft = 16384
fs = 2

b = approximate_b(sll)
win = fixed_point_kaiser(M, b, nbits)
fname = f'kaiser_win_{M:d}_pts_{b:.0f}_beta.vhd'
cname = 'C_KAISER_{M:d}_LUT'
write_out_window(win, fname, nbits, cname)
sp, freq = sg.gen_full_spectrum(win, nfft, fs)
sp_r, freq_r = sg.gen_full_spectrum(np.round(win), nfft, fs)
sg.plot_window_spectrum(sp, freq, sp_r, freq_r)
#sg.plot_sig(win, 1)
win2 = fixed_point_kaiser2(M, b, nbits)
sp2, freq2 = sg.gen_full_spectrum(win2, nfft, fs)
sp_r2, freq_r2 = sg.gen_full_spectrum(np.round(win2), nfft, fs)
sg.plot_window_spectrum(sp2, freq2, sp_r2, freq_r2)
sg.plot_sig(win2, 1)
