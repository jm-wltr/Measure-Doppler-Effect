Created on Sat Nov  6 13:26:52 2021
@author: jaime
"""

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
    RATE = 48000
    div = 5
    CHUNK = int(RATE/div)
    stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)
    
    #fig, ax = plt.subplots(figsize=(10,6))
    fig = plt.figure()
    ax = fig.add_subplot(211, title = "Audio wave", xlabel = "Time (ms)")
    ax2 = fig.add_subplot(212, title = "Fourier transform", xlabel = "Frequency (Hz)")
    time = np.linspace(0, 1000/div, num = CHUNK)
    freq = np.linspace(0, RATE, num = CHUNK)
    ax.set_ylim(-15000, 15000)
    ax2.set_ylim(0, 10000000)
    ax.set_xlim(0, 1000/div) #make sure our x axis matched our chunk size
    ax2.set_xlim(0, RATE/2)
    line, = ax.plot(time, np.random.rand(CHUNK))
    line2, = ax2.plot(freq, np.random.rand(CHUNK))
    ax.set_yticks([])
    ax2.set_yticks([])
    plt.tight_layout()
    
    while True:
        data = np.frombuffer(stream.read(CHUNK), np.int16)
        fourier = np.abs(np.fft.fft(data))
        line.set_ydata(data)
        line2.set_ydata(fourier)
        i = 2
        peaks = []
        indices = []
        while i <= len(fourier)/2-3:
            if fourier[i] > fourier[i-2] \
            and fourier[i] > fourier[i-1] \
            and fourier[i] > fourier [i+1] \
            and fourier[i] > fourier[i+2]:
                peaks.append(fourier[i])
                indices.append(i)
            i = i + 1
        peak = max(peaks)
        index = peaks.index(peak)
        print(indices[index]*div)
        print(peak)
        print()
            
        plt.pause(0.0001)
        
if __name__ == '__main__':
    main()
