import numpy as np
from scipy import signal
from scipy import special
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
    kaiser_win = (2**nbits-1)*kaiser(M,beta)
    return kaiser_win

def kaiser(M, beta, sym=False):
    win = signal.windows.kaiser(M, beta, sym)
    return win

def fixed_point_kaiser2(M, beta, nbits):
    kaiser_win = (2**nbits-1)*kaiser2(M,beta)
    return kaiser_win

def kaiser2(M, beta):
    n_array = np.arange(M)
    gd = M/2
    arg = beta*(1-((n_array-gd)/gd)**2)**0.5
    win = special.i0(arg)/special.i0(beta)
    return win

def write_out_window(win, fname, nbits, cname):
    print('writing out coefficient file ' + fname)
    win = np.round(win)
    assert max(win) < 2**nbits, 'ERROR: Maximum value for window cannot be contained in nbits. Reduce window amplitude or increase bit width'
    win = [ int(coe) for coe in win ]
    for coe in range(len(win)):
        if win[coe] < 0:
            win[coe] = (win[coe] ^ 2**nbits-1) + 1
    with open(fname,'w') as f_handle:
        print(f'type lut is array (natural range 0 to {len(win)-1}) of std_logic_vector({nbits-1} downto 0);', file=f_handle)
        print(f'constant {cname} : lut := (', file=f_handle)
        for coe in win[:-1]:
            print(f'"{abs(coe):0>{nbits}b}",', file=f_handle)
        print(f'"{abs(win[-1]):0>{nbits}b}");', file=f_handle)

def write_out_coe(response, fname):
    print('Writing out coefficient file as string of ints: ' + fname)
    response = np.round(response)
    response = [ int(coe) for coe in response ]
    with open(fname, 'w') as f_handle:
        print('radix=10;', file=f_handle)
        print('coefdata=', file=f_handle)
        for coe in response[:-1]:
            print(f'{coe},', file=f_handle)
        print(f'{response[-1]};', file=f_handle)


