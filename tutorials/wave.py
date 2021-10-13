#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
From tutorial https://www.youtube.com/watch?v=AShHJdSIxkY
"""

## Use Tkinter backend for matplotlib

import pyaudio # use "conda install pyaudio" to install
import wave
from array import array
import struct
import numpy as np
import matplotlib.pyplot as plt


CHUNK = 1024 * 4
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)

data = stream.read(CHUNK)
data_int = np.array(struct.unpack(str(2 * CHUNK) + "B", data), dtype="b") + 127

fig, ax = plt.subplots()
ax.plot(data_int, "-")
plt.show()
