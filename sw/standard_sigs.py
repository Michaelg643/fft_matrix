#!/usr/bin/python3
import sig_gen as sg
from matplotlib import pyplot as plt

duration = 1 # seconds
max_freq = 20e3
min_freq = 20
npts = 64
fs = 44100
nfft = 32768

x1 = sg.gen_chirp(min_freq,max_freq, 'real', duration, fs)
#sg.plot_sig(x1,fs,0.25)
sp, freq = sg.gen_spectrum(x1,nfft, fs)
freq_dict_array = sg.determine_bins(freq, npts, min_freq, 20e3)
sp_norm, freq_norm = sg.freq_int(sp, freq, freq_dict_array)
#sg.print_freq_dict_array(freq_dict_array, freq)
sg.plot_spectrum(sp,freq, sp_norm, freq_norm, fs)
plt.show()
