#!/usr/bin/python
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

#import stuffr
#import chirp_config
#from optparse import OptionParser

# remove the any residual band specific variation in noise floor
# that isn't removed by the amplitude domain adaptive filter before chirp downconversion.
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
sr = 50e6 / 500
window = 8192
f = 'data/out/dmixed.out'
if os.path.isfile("%s.png" % (f)):
    print('File already exists, overwritting')

z = np.fromfile(f, dtype=np.complex64)

S = spectrogram(z, window=window)
S = medianEqualize(S)
freq = np.linspace(0, (len(z) / sr) * cr, num=S.shape[0]) / 1e6
vrange = np.linspace(3e8 * (-(sr / 2)) / cr, 3e8 * (sr / 2.0) / cr, num=S.shape[1]) / 1e3

cdb = np.transpose(comprz_dB(S[:, ::-1]))
plt.pcolormesh(np.linspace(0, 1, cdb.shape[1]), np.linspace(0, 1, cdb.shape[0]), cdb, cmap="jet", vmin=-1.0)

#plt.ylim([7500, 17500])
#plt.xlim([0, (len(z) / sr) * cr])
plt.xlabel("Frequency (MHz)")
plt.ylabel("Virtual range (km)")
plt.title(f)
plt.tight_layout()
plt.colorbar()
plt.savefig('data/out/dmixed.png')
plt.clf()

plt.close()
