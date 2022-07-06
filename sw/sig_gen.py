import numpy as np
from numpy.fft import fft, fftfreq, fftshift
from matplotlib import pyplot as plt

def gen_chirp(start_freq, stop_freq, dtype, duration, fs, filename=None):
    """
        Description: Generate a Linear frequency chirp
        Parameters:
            start_freq - Start frequency (analog)
            stop_freq - Stop frequency (analog)
            dtype - complex or real
            duration - time in seconds to generate
            fs - sampling frequency
            filename - input filename if we need to save this off.
        Returns:
            a numpy array containing the samples of the waveform
    """
    num_samps = int(duration*fs)
    sig = np.zeros(num_samps)
    samp_idx_arr = np.arange(num_samps)
    start_freq_norm = start_freq/fs
    stop_freq_norm = stop_freq/fs

    chirp_rate = (stop_freq_norm - start_freq_norm)/num_samps
    arg = 2*np.pi*(start_freq_norm+chirp_rate/2*samp_idx_arr)
    if dtype == 'real':
        sig = np.cos(arg*samp_idx_arr)
    else:
        sig = np.exp(1j*arg*samp_idx_arr)

    return sig

def plot_sig(sig, fs, frac=1, title=None):
    num_samps = int(frac*len(sig))
    samp_idx_arr = np.arange(num_samps)
    time_idx_arr = samp_idx_arr/fs
    sig_re = sig.real

    if np.iscomplexobj(sig):
        plt.subplot(2,1,1)
    
    plt.stem(time_idx_arr, sig_re[samp_idx_arr])
    if title is not None:
        plt.title(title)
    
    if np.iscomplexobj(sig):
        sig_im = sig.imag
        plt.subplot(2,1,2)
        plt.plot(time_idx_arr, sig_im[samp_idx_arr])
    plt.show()

def determine_bins(raw_freq, npts, min_freq, max_freq):
    # create the fft sections required for the rgb matrix. perform frequency integration on bins
    # step 1: determine bin centers:
    log_max_freq = np.log10(max_freq)
    log_min_freq = np.log10(min_freq)
    log_freq_array = np.linspace(log_min_freq, log_max_freq, npts)
    freq_array = 10**log_freq_array
    print('Center freqs for matrix: ' + str(freq_array))


    #step 2: determine indexes to integrate
    # minimize distance from optimal freq_array point to what is available in the matrix
    freq_dict_array = []
    for freq in freq_array:
        freq_dict = {}
        freq_dict['freq'] = freq
        current_diff_array = np.abs(raw_freq - freq)
        min_freq_delta = np.amin(current_diff_array)
        freq_dict['closest_idx'] = np.where(current_diff_array == min_freq_delta)[0]
        freq_dict['closest_fft_freq'] = raw_freq[freq_dict['closest_idx']]
        freq_dict['freq_delta'] = np.abs(freq_dict['closest_fft_freq'] - freq_dict['freq'])[0]
        freq_dict_array.append(freq_dict)

    # step 3: determine bins to sum over; start and stop bin indicies
    first_flag = True
    array_len = len(freq_dict_array)
    usable_fft_pts = int(len(raw_freq) - 1)
    for i in range(array_len):
        if first_flag is True:
            first_flag = False
            freq_dict_array[i]['start_idx'] = 0
        else:
            freq_dict_array[i]['start_idx'] = int(freq_dict_array[i-1]['stop_idx'])

        if i < (array_len - 1):
            dist_to_next = freq_dict_array[i+1]['closest_idx'] - freq_dict_array[i]['closest_idx']
            freq_dict_array[i]['stop_idx'] = int(freq_dict_array[i]['closest_idx'] + np.round(dist_to_next/2))
        else:
            freq_dict_array[i]['stop_idx'] = usable_fft_pts

        freq_dict_array[i]['sum_length'] = int(freq_dict_array[i]['stop_idx'] - freq_dict_array[i]['start_idx'] + 1)
    return freq_dict_array

def freq_int(sp, freq, freq_dict_array):
    # step 4: sum over these bin indicies (bindicies?) and normalize
    sp_norm = []
    freq_norm = []
    for freq_dict in freq_dict_array:
        start = freq_dict['start_idx']
        stop = freq_dict['stop_idx']
        start_freq = freq[start]
        stop_freq = freq[stop]
        bw = stop_freq - start_freq
        #print('start index: ' + str(start))
        #print('stop index: ' + str(stop))
        #print('start freq: ' + str(start_freq))
        #print('stop freq: ' + str(stop_freq))
        #print('Bandwidth: ' + str(bw))
        sum_length = freq_dict['sum_length']
        center_freq = freq_dict['freq']
        #sp_of_interest = np.split(sp, [start, stop])[0]
        sp_of_interest = sp[start:stop]
        #print(np.abs(sp_of_interest))
        sp_int = np.sum(np.abs(sp_of_interest))/bw
        #print('Pre normalized sum: ' + str(sp_int*bw))
        #print('normalized sum: ' + str(sp_int))
        sp_norm.append(sp_int)
        freq_norm.append(center_freq)
        #print()
    return sp_norm, freq_norm

def print_freq_dict_array(freq_dict_array, raw_freq):
    for freq_dict in freq_dict_array:
        print('freq: ' + str(freq_dict['freq']))
        print('current_closest_idx (bin index): ' + str(freq_dict['closest_idx']))
        print('Closest fft frequency: ' + str(freq_dict['closest_fft_freq']))
        print('Frequency delta: ' + str(freq_dict['freq_delta']))
        print('Start index: ' + str(freq_dict['start_idx']))
        print('Start freq: ' + str(raw_freq[freq_dict['start_idx']]))
        print('Stop index: ' + str(freq_dict['stop_idx']))
        print('Stop freq: ' + str(raw_freq[freq_dict['stop_idx']]))
        print('sum_length: ' + str(freq_dict['sum_length']))
        print()

def gen_half_spectrum(sig, nfft, fs):
    sp,freq = gen_full_spectrum(sig,nfft,fs)
    sp = sp[0:int(nfft/2)]
    freq = freq[0:int(nfft/2)]
    return sp,freq

def gen_full_spectrum(sig, nfft, fs):
    sp = fft(sig, nfft, axis=0)*fs/nfft
    freq = fftfreq(nfft, 1/fs)
    return sp,freq

def plot_window_spectrum(sp, freq, sp_r=None, freq_r=None):
    if sp_r is not None:
        plt.subplot(2,1,1)
    sp = fftshift(sp)
    freq = fftshift(freq)
    amp = 20*np.log10(np.abs(sp)/np.max(np.abs(sp)))
    plt.plot(freq, amp)
    plt.title('Floating point (ideal) case')

    if sp_r is not None:
        plt.subplot(2,1,2)
        sp_r = fftshift(sp_r)
        freq_r = fftshift(freq_r)
        amp_r = 20*np.log10(np.abs(sp_r)/max(np.abs(sp_r)))
        plt.plot(freq_r, amp_r)
        plt.title('Fixed point (actual) case')
    plt.show()

def plot_spectrum(fs, sp, freq, sp_norm, freq_norm):
    plt.subplot(2,1,1)
    plt.plot(freq,abs(sp))
    plt.title('ideal fft response')
    plt.xscale('log')
    plt.xlim(20,fs/2)

    plt.subplot(2,1,2)
    plt.bar(freq_norm[:-1], sp_norm[:-1], width=np.diff(freq_norm), ec="k", align="edge")
    #plt.bar(freq_norm, sp_norm)
    plt.xscale('log')
    plt.title('approximate fft response')
    plt.xlabel('frequency [Hz]')
    plt.xlim(20,fs/2)
    plt.show()
