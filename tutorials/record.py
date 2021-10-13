#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
From tutorial https://youtu.be/jbKJaHw0yo8
"""

import pyaudio # use "conda install pyaduio" to install
import wave
from array import array
from struct import pack


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5

p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                frames_per_buffer = CHUNK)

print("* recording")

frames = []

for i in range(0, int(RATE/CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
    
print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open("output1.wav", "wb")
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
