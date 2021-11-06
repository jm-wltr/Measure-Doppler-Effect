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
      
    """
    ------- Here are the values you can adjust to your liking -------
    """
    RATE = 48000 #Number of samples per second
    div = 5 #RATE/div = CHUNK (number of samples displayed each time)
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
        i = int(low_end/div)
        
        if i <2:
            i = 2
        if int(high_end/div) > int(CHUNK/2)-3:
            high_end = int(CHUNK/2)-3
            
        peaks = []
        indices = []
        while i <= int(high_end/div):
            if fourier[i] > fourier[i-1] and fourier[i] > fourier[i+1]:
                #and fourier[i] > fourier[i-2] \
                    #and fourier[i] > fourier [i+2] \
            
                peaks.append(fourier[i])
                indices.append(i)
            i = i + 1
        try:
            peak = max(peaks)
            index = peaks.index(peak)
            print(indices[index]*div)
            print(peak)
        except ValueError:
            print("NaN")
            print("NaN")
            pass

        print()
            
        plt.pause(0.0001)
        
if __name__ == '__main__':
    main()
