#!/usr/bin/python3
################################################################################
# Date: June 30, 2022
# Engineer: Michael
# Company: Idea machines
################################################################################
import numpy as np
from numpy.fft import fft, fftfreq, fftshift
from window import *
from sig_gen import *

def discrete_hilbert(length, sll):
    # calculates the impulse response of a hilbert transform
    # Eq 12.67 in discrete-time signal processing, Oppenheim
    thresh = 1e-12
    b = approximate_b(sll)
    gd = int(length/2)
    window = kaiser(length, b,sym=True)
    hilbert = np.zeros((length,))
    for samp in np.arange(length):
        if samp != int(gd):
            hilbert[samp] = window[samp]*2/np.pi*np.sin(np.pi*(samp-gd)/2)**2/(samp-gd)
        else:
            hilbert[samp] = 0

    # zero out anything not zero already:
    for samp in np.arange(length):
        if np.abs(hilbert[samp]) < thresh:
            hilbert[samp] = 0
    return hilbert

def fixed_point_hilbert(length, sll, nbits):
    fixed_hilbert = (2**(nbits-1)-1)*discrete_hilbert(length, sll)
    return fixed_hilbert

if __name__ == "__main__":
    n = 125
    hilbert_len = int(4*n+3) # per FIR compiler rules for hilbert transform length
    start_freq = 20e0
    stop_freq = 20e3
    dtype = 'real'
    duration = 1
    fs = 44100
    samp_diff = hilbert_len - 1
    samp_off = int(samp_diff/2)
    sll = 40
    nbits = 16
    ds_factor = 2
    nfft = 32768
    nfft_ds = int(nfft/ds_factor)

    hilbert = discrete_hilbert(hilbert_len, sll)
    
    title = f"Hilbert transform impulse response of length {hilbert_len}"
    print(title)
    plot_sig(hilbert,1, title=title)
    sp, freq = gen_full_spectrum(hilbert, nfft,fs)
    plot_window_spectrum(sp,freq)

    print('Generating sine wave')
    rsig = gen_chirp(start_freq, stop_freq, dtype, duration, fs)
    rsig_l = len(rsig)
    print('generating complex representation')
    isig = np.convolve(rsig, hilbert)
    print('Length of rsig: ' + str(len(rsig)))
    print('Length of isig: ' + str(len(isig)))
    #plt.plot(np.arange(rsig_l), rsig, label='Real (original) signal')
    #plt.plot(np.arange(rsig_l), isig[samp_off:len(isig)-samp_off], label='Imaginary (hilbert transform of original) signal')
    #plt.legend(loc="upper right")
    #plt.show()

    #fname_vhd = f'hilbert_transform_taps_{hilbert_len}pts_{nbits}b.vhd'
    fname_coe = f'hilbert_transform_taps_{hilbert_len}pts.coe'
    cname = 'C_HILBERT_LUT'
    hilbert_fix = fixed_point_hilbert(hilbert_len, sll, nbits)
    #print(hilbert_fix)
    #write_out_window(hilbert_fix, fname_vhd, nbits, cname)
    write_out_coe(hilbert_fix, fname_coe)

    #compare spectrums now.
    freq = fftshift(fftfreq(nfft,1/fs))
    freq_d2 = fftshift(fftfreq(nfft_ds,2/fs))
    generated_re = rsig
    gr_fft = 20*np.log10(np.abs(fftshift(fft(generated_re, nfft)*fs/nfft)))
    artificial_cx = rsig + 1j*isig[samp_off:len(isig)-samp_off]
    ac_fft = 20*np.log10(np.abs(fftshift(fft(artificial_cx, nfft)*fs/nfft)))
    generated_cx = gen_chirp(start_freq, stop_freq, 'imag', duration, fs)
    gc_fft = 20*np.log10(np.abs(fftshift(fft(generated_cx, nfft)*fs/nfft)))

    # Generated real, should have two parts
    plt.subplot(3,1,1)
    plt.plot(freq, gr_fft)
    plt.title('Generated real signal')

    # artifical complex, should have one part
    plt.subplot(3,1,2)
    plt.plot(freq, ac_fft)
    plt.title('Artificial Complex signal')

    # generated complex, should have one part
    plt.subplot(3,1,3)
    plt.plot(freq, gc_fft)
    plt.title('Generated Complex signal')
    plt.show()

    print('Downsampling artifical complex by 2')
    ac_d2 = artificial_cx[0::2]
    #shift by fs/2 by multiplying every other sample by -1
    ac_d2[::2] = [x*-1 for x in ac_d2[::2]]
    ac_d2_fft = 20*np.log10(np.abs(fftshift(fft(ac_d2,nfft_ds)*fs/(2*nfft_ds))))

    # artifical complex, should have one part
    plt.subplot(2,1,1)
    plt.plot(freq, ac_fft)
    plt.title('Artificial Complex signal')
    plt.xlim(0,fs/2)
    
    plt.subplot(2,1,2)
    plt.plot(freq_d2, ac_d2_fft)
    plt.xlim(-fs/4,fs/4)
    plt.title('Artifical Complex signal (downsampled by 2 & shifted by fs/2)')
    plt.show()

