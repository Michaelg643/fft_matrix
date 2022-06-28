import numpy as np
from scipy import signal
def approximate_b(A_sl):
    """From eq 10.13 in Discrete Time Signal Processing, oppenheim, 3rd edition"""
    assert ((A_sl > 0) and (A_sl <= 120)), f'A_sl needs to be between 0 and 120, got {A_sl}'
    if A_sl <= 13.26:
        b = 0
    elif (13.26 < A_sl) and (A_sl <= 60):
        b = 0.76609*(A_sl - 13.26)**0.4 + 0.09834*(A_sl - 13.26)
    elif (60 < A_sl) and (A_sl <= 120):
        b = 0.12438*(A_sl + 6.3)
    print('Using a b of ' + str(b))
    return b

def fixed_point_kaiser(M, beta, nbits):
    kaiser_win = (2**nbits)*kaiser(M,beta)
    #kaiser_win = np.round((2**nbits)*kaiser(M,beta))
    return kaiser_win

def kaiser(M, beta, sym=False):
    win = signal.windows.kaiser(M, beta, sym=False)
    return win
