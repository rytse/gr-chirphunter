import matplotlib

matplotlib.use("Agg")

import numpy as np
from numpy.fft import *

import scipy.signal
import matplotlib.pyplot as plt

import math
import glob
import sys
import os
import sys

def medianEqualize(S):
    for i in np.arange(S.shape[0]):
        S[i, :] = S[i, :] / np.median(S[i, :])
    return (S)


def hanning(L=1000):
    n = np.linspace(0.0,L-1,num=L)
    return(0.5*(1.0-np.cos(2.0*np.pi*n/L)))


def comprz(x):
    """ Compress signal in such a way that elements less than zero are set to zero. """
    zv = x*0.0
    return(np.where(x>0,x,zv))


def comprz_dB(xx,fr=0.05):
    """ Compress signal in such a way that is logarithmic but also avoids negative values """
    x = np.copy(xx)
    sh = xx.shape
    x = x.reshape(-1)
    x = comprz(x)
    x = np.setdiff1d(x,np.array([0.0]))
    xs = np.sort(x)
    mini = xs[int(fr*len(x))]
    mn = np.ones_like(xx)*mini
    xx = np.where(xx > mini, xx, mn)
    xx = xx.reshape(sh)
    return(10.0*np.log10(xx))


def spectrogram(x,window=1024,wf=hanning):
    wfv = wf(L=window)
    Nwindow = int(math.floor(len(x)/window))
    res = np.zeros([Nwindow,window])
    for i in range(Nwindow):
        res[i,] = np.abs(fftshift(fft(wfv*x[i*window + np.arange(window)])))**2
    return(res)

cr = 1.0085e5
#cr = 0.1e6
sr = 50e6 / 500
#sr = 20e6 / 500
#window = 2**18
window = 2**13

if len(sys.argv) == 2:
    fn = sys.argv[1]
else:
    fn = 'dmixed.out'
path = f'data/out/{fn}'

z = np.fromfile(path, dtype=np.complex64)

S = spectrogram(z, window=window)
S = medianEqualize(S)
freq = np.linspace(0, (len(z) / sr) * cr, num=S.shape[0]) / 1e6
vrange = np.linspace(3e8 * (-(sr / 2)) / cr, 3e8 * (sr / 2.0) / cr, num=S.shape[1]) / 1e3

cdb = np.transpose(comprz_dB(S[:, ::-1]))
plt.pcolormesh(np.linspace(0, 1, cdb.shape[1]), np.linspace(0, 1, cdb.shape[0]), cdb, cmap="jet", vmin=-1.0)
#plt.pcolormesh(freq, vrange, cdb, cmap="jet", vmin=-1.0)

#plt.ylim([0e3, 1e3])
#plt.xlim([0, 40])
plt.xlabel("Frequency (MHz)")
plt.ylabel("Virtual range (km)")
plt.title(f)
plt.tight_layout()
plt.colorbar()
plt.savefig(f'{path}.png')
plt.clf()

plt.close()
