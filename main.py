# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 20:00:55 2021

@author: jaime
"""

import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np

def main():
    mic = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 25000
    CHUNK = int(RATE/40)
    stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)
    
    #fig, ax = plt.subplots(figsize=(10,6))
    fig = plt.figure()
    ax = fig.add_subplot(211)
    ax2 = fig.add_subplot(212)
    x = np.arange(0, 2 * CHUNK, 2)
    ax.set_ylim(-15000, 15000)
    ax2.set_ylim(0, 10000000)
    ax.set_xlim(0, CHUNK*2) #make sure our x axis matched our chunk size
    ax2.set_xlim(0, CHUNK)
    line, = ax.plot(x, np.random.rand(CHUNK))
    line2, = ax2.plot(x, np.random.rand(CHUNK))
    
    while True:
        data = np.frombuffer(stream.read(CHUNK), np.int16)
        fourier = np.abs(np.fft.fft(data))
        i = 0
        for n in fourier:
            if fourier[i] < 10000:
                fourier[i] = 0
            i += 1
        data = np.fft.ifft(fourier)
        line.set_ydata(data)
        line2.set_ydata(fourier)
        plt.pause(0.0001)
        
if __name__ == '__main__':
    main()
