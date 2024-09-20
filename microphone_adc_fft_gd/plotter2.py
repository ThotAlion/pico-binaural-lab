import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import serial
import numpy as np

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
# Set up the serial connection (adjust 'COM3' to your serial port and baud rate)
port = "COM6"
ser = serial.Serial(port, 115200, timeout=1)
# Initialize empty data lists for the axes
data1 = [0] * 128
data2 = [0] * 128

fig, (ax1, ax2) = plt.subplots(2, 1)

line1, = ax1.plot(data1, color='blue')
line2, = ax2.plot(data2, color='red')
ax1.clear()
ax1.set_title('Magnitude')
ax1.set_ylim(0, 10000)
ax1.set_xlim(0, 128)
ax1.grid(True)
ax2.clear()
ax2.set_title('Phase')
ax2.set_ylim(-200,200)
ax2.set_xlim(0, 128)
ax2.grid(True)


def update(frame):
    """Update the plots with new data."""
    global data1, data2

    if ser.in_waiting:
        line = ser.readline().decode('utf-8').strip('\t')
        if line:
            if line[0] == 'M':
                data1 = convertir_chaine_en_entiers(line)
                line1.set_ydata(data1)
                line1.set_xdata(range(len(data1)))
            elif line[0] == 'P':
                data2 = convertir_chaine_en_entiers(line)
                line2.set_ydata(data2)
                line2.set_xdata(range(len(data2)))

    return line1, line2

ani = FuncAnimation(fig, update, blit=True, interval=10)

plt.tight_layout()
plt.show()