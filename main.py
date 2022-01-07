# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 20:00:55 2021
@author: jaime
"""

import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import pyautogui
import time as tm
      
def main():
      
    """
    ------- Here are the values you can adjust to your liking -------
    """
    RATE = 48000 #Number of samples per second
    div = 5 #RATE/div = CHUNK (number of samples displayed each time)
    amplitude = 15000 #maximum value of the y axis of the audio wave graph
    volume = 40000 #maximum value of the y axis of the fourier transform graph
    CHUNK = int(RATE/div) # Number of samples displayed each time (DO NOT MODIFY)
    low_end = 20000 #minimum frequency that can be displayer in the console as tallest peak. Remeber it has to be an int.
    high_end = 20300 #maximum frequency that can be displayed in the console as tallest peak.
    """
    -----------------------------------------------------------------
    """

    start = 0
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
    ax2.set_xlim(20000,20300)
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
        if i <0:
            i = 0
        if int(high_end/div) >= int(len(fourier)/2)-3:
            high_end = int(len(fourier)/2)

        peak = max(fourier[i:int(high_end/div)])
        index = i + int(list(fourier[i:int(high_end/div)]).index(peak))
        print(peak)
        print(index*div)

        print()
        
        if tm.time() - start > 0.4:
            if index*div > 20170:
                pyautogui.write("up ")
                start = tm.time()
            elif index*div < 20140:
                pyautogui.write("down ")  
                start = tm.time()
           
        plt.pause(0.001)
         
if __name__ == '__main__':
    main()
    
