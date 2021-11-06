# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 20:00:55 2021
@author: jaime
"""

import pyaudio
import struct
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

def main():
      
    """
    ------- Here are the values you can adjust to your liking -------
    """
    RATE = 48000 #Number of samples per second
    div = 1 #RATE/div = CHUNK (number of samples displayed each time)
    amplitude = 15000 #maximum value of the y axis of the audio wave graph
    volume = 30000 #maximum value of the y axis of the fourier transform graph
    CHUNK = int(RATE/div) # Number of samples displayed each time (DO NOT MODIFY)
    low_end = 1000 #minimum frequency that can be displayer in the console as tallest peak. Remeber it has to be an int.
    high_end = 25000 #maximum frequency that can be displayed in the console as tallest peak.
    """
    -----------------------------------------------------------------
    """

    #Define the rest of the variables needed for recording audio and start recording
    mic = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1

    stream = mic.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, output=True, frames_per_buffer=CHUNK)

    #Create plots
    fig = plt.figure()
    
    ax = fig.add_subplot(211, title = "Audio wave", xlabel = "Time (ms)")
    ax2 = fig.add_subplot(212, title = "Fourier transform", xlabel = "Frequency (Hz)")
    
    time = np.linspace(0, 1000/div, num = CHUNK)
    freq = np.linspace(0, RATE, num = CHUNK)

    ax.set_xlim(0, 1000/div)
    ax2.set_xlim(0, RATE/2)
    ax.set_ylim(-amplitude, amplitude)
    ax2.set_ylim(0, volume)

    ax.set_yticks([])
    ax2.set_yticks([])
    
    line, = ax.plot(time, np.random.rand(CHUNK))
    line2, = ax2.plot(freq, np.random.rand(CHUNK))

    plt.tight_layout()
    
    
    while True:
        #Update the plot
        data = np.frombuffer(stream.read(CHUNK), np.int16)
        fourier = np.abs(np.fft.fft(data))
        line.set_ydata(data)
        line2.set_ydata(fourier)
        
        #Display frequency of largest peak
        indices = sig.find_peaks(fourier[0:int(len(fourier)/2)])
        peaks = []
        for i in indices[0]:
            peaks.append(fourier[i])
        peak = max(peaks)
        index = peaks.index(peak)
        print(indices[0][index]*div)
        print(peak)
        print()
        plt.pause(0.0001)
        
if __name__ == '__main__':
    main()
