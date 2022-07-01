################################################################################
# Date: June 30, 2022
# Engineer: Michael
# Company: Idea machines
################################################################################
import numpy as np
from window import *
from sig_gen import *

def discrete_hilbert(n):
    # calculates the impulse response of a hilbert transform
    # Eq 12.67 in discrete-time signal processing, Oppenheim
    b = approximate_b(80)
    gd = n/2
    window = kaiser((n-gd), b, sym=False)
    samp_array = np.arange(n)
    hilbert = window*2/np.pi*np.sin(np.pi*(samp_array-gd)/2)/(samp_array-gd)
    plot_sig(hilbert,2)
    
