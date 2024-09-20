#!/usr/bin/env python3

# Grabs raw data from the Pico's UART and plots it as received

# Install dependencies:
# python3 -m pip install pyserial matplotlib

# Usage: python3 plotter <port>
# eg. python3 plotter /dev/ttyACM0

# see matplotlib animation API for more: https://matplotlib.org/stable/api/animation_api.html

import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.lines import Line2D

def convertir_chaine_en_entiers(chaine):
    result = []
    elements = chaine.split("\t")  # Sépare la chaîne par les tabulations
    
    for element in elements:
        try:
            nombre = int(element)  # Tente de convertir en entier
            result.append(nombre)
        except ValueError:
            pass
    
    return result

# disable toolbar
plt.rcParams['toolbar'] = 'None'

class Plotter:
    def __init__(self, ax):
        print(ax)
        self.ax1 = ax[0]
        self.ax2 = ax[1]
        self.fdata = [0]
        self.mdata = [0]
        self.pdata = [0]
        self.lineM = Line2D(self.fdata, self.mdata)
        self.lineP = Line2D(self.fdata, self.pdata)

        self.ax1.add_line(self.lineM)
        self.ax1.set_ylim(0, 10000)
        self.ax1.set_xlim(0, 5000)
        self.ax1.set_xticks(range(0, 5000, 250))
        self.ax1.grid(True)
        self.ax2.add_line(self.lineP)
        self.ax2.set_ylim(-200,200)
        self.ax2.set_xlim(0, 5000)
        self.ax2.set_xticks(range(0, 5000, 250))
        self.ax2.grid(True)
        

    def update(self, y):
        self.fdata = [i * 5000/128 for i in range(len(y))]
        self.mdata = y
        self.lineM.set_data(self.fdata, self.mdata)
        return self.lineM,self.lineP


def serial_getter():
    # grab fresh ADC values
    # note sometimes UART drops chars so we try a max of 5 times
    # to get proper data
    while True:
        for i in range(5):
            try:
                line = ser.readline().decode("utf-8")
                print(line)
                liste_entiers =convertir_chaine_en_entiers(line)
                print(liste_entiers)
                break
            except ValueError:
                continue
        yield liste_entiers

port = "COM6"
ser = serial.Serial(port, 115200, timeout=1)

fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(6, 8))
plotter = Plotter([ax1,ax2])

ani = animation.FuncAnimation(fig, plotter.update, serial_getter, interval=1,
                              blit=True, cache_frame_data=False)

ax1.set_xlabel("Frequency")
ax2.set_xlabel("Frequency")
ax1.set_ylabel("Amplitude")
ax2.set_ylabel("Phase (degrees)")
fig.canvas.manager.set_window_title('Microphone ADC example')
fig.tight_layout()
plt.show()
