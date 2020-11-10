import tkinter
from tkinter import *
import math
import wave
import numpy as np
import matplotlib.pyplot as plot
import pyaudio
import struct
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import scipy.io.wavfile
from tkinter import filedialog as fd

#--------------define Global Variable------------
freqNote = {'C':130.81, 'C#':138.59, 'D':146.83, 'D#':155.56, 'E':164.81, 'F':174.61
            , 'F#':185, 'G':196, 'G#':207.65, 'A':220, 'A#':233.08, 'B':246.94}
listnote = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
columnpos = [0,0,1,1,2,3,3,4,4,5,5,6]
totalwave = []
active='red'
default_color='white'

def playnote(freq,recordstatus):
    p = pyaudio.PyAudio()
    # volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = 1.0  # in seconds, may be float
    f = freq  # sine frequency, Hz, may be float
    # generate samples, note conversion to float32 array
    period = fs/f
    timelist = np.arange(fs * duration)
    samples = (np.sin(2 * np.pi * timelist * 1/period)).astype(np.float32)
    plot(timelist, samples, period)
    if recordstatus['bg'] == active:
        totalwave.append(samples)
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    # play. May repeat with different volume values (if done interactively)
    stream.write(samples)
    stream.stop_stream()
    stream.close()
    p.terminate()

def plot(timelist, valuelist, period):
    x = timelist[0:int(period)*2]
    y = valuelist[0:int(period)*2]
    fig = Figure(figsize=(4,3))
    a = fig.add_subplot(111)
    a.plot(x, y, color='red')
    a.set_ylabel("Y")
    a.set_xlabel("sampling rate")
    canvas = FigureCanvasTkAgg(fig, master=Graph)
    canvas.get_tk_widget().grid(row=0)
    canvas.draw()

def RecordFUNC(btn):
    if (btn['bg'] == active):
        btn['bg'] = default_color
    else:
        btn['bg'] = active

def Playrecord():
    p = pyaudio.PyAudio()
    # volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32, channels=1, rate=fs, output=True)
    # play. May repeat with different volume values (if done interactively)
    for i in totalwave:
        stream.write(i)
    stream.stop_stream()
    stream.close()
    p.terminate()

def savefile():
    name = fd.asksaveasfile(mode='w', defaultextension=".wav")
    print(name.name)
    y = np.asarray(totalwave).ravel()
    fs = 44100 # hertz
    scipy.io.wavfile.write(name.name, fs, y)

def clearrecord():
    totalwave.clear()

#-----------------main-----------------
root = Tk()
root.title('Hello Piano')
root.config(bg='lightgray')

# Create frame piano
piano = Frame(root, width=800, height=400, bg='white')
piano.grid(row=0, columnspan=2, padx=10, pady=10)

# Create frame Record
Record = Frame(root, width=400, height=200, bg='light blue')
Record.grid(row=1, column=0, pady=10)

# Create frame Graph
Graph = Frame(root, width=400, height=300, bg='gray')
Graph.grid(row=1, column=1, pady=10)

# Create Button to Record
rec_btn = Button(Record, bg = default_color, fg = 'black', text='Record', height=20, width=10,
                 command = lambda : RecordFUNC(rec_btn))
rec_btn.grid(row=0, column=0)

clear_btn = Button(Record, bg = default_color, fg = 'black', text='Clear', height=20, width=10,
                 command = clearrecord)
clear_btn.grid(row=0, column=1)

play_btn = Button(Record, bg = default_color, fg = 'black', text='Play', height=20, width=10,
                 command = lambda : Playrecord())
play_btn.grid(row=0, column=2)

save_btn = Button(Record, bg = default_color, fg = 'black', text='Save', height=20, width=10,
                 command = lambda : savefile())
save_btn.grid(row=0, column=3)


# Create Button in piano
for x in range(3,6):
    for y in range(12):
        counter_column = columnpos[y] + (7 * (x-1))
        if (y == 0) or (y == 2) or (y == 4) or (y == 5) or (y == 7) or (y == 9) or (y == 11):
            btn = Button(piano, bg="white", text=listnote[y] + str(x), height=10, width=4,
                         command=lambda freq=freqNote[listnote[y]] * (2 ** (x - 3)): playnote(freq,rec_btn))
            btn.grid(row=1, column=counter_column)
        else :
            a = y
            btn = Button(piano, bg="black", fg="white", text=listnote[y] + str(x), height=10, width=3,
                         command=lambda freq=freqNote[listnote[y]] * (2 ** (x - 3)): playnote(freq,rec_btn))
            btn.grid(row=0, column=counter_column, columnspan=2)



root.mainloop()


