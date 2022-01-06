from picoThread import PicovoiceThread as picoT
import argparse

# Create a GUI using Tkinter
import tkinter as tk

parser = argparse.ArgumentParser()

parser.add_argument(
    '--access_key',
    help='AccessKey obtained from Picovoice Console (https://picovoice.ai/console/)', 
    required=True)

args = parser.parse_args()

window = tk.Tk()
window.title("Pico Testing")
window.minsize(width=400, height=200)

timeLabel = tk.Label(window, text='00 : 00 : 00', font=("Arial", 80))
timeLabel.pack(fill=tk.BOTH, pady=90)

picoThread = picoT(timeLabel, args.access_key)

def onClose():
    picoThread.stop()
    while not picoThread.is_stopped():
        pass
    window.destroy()

window.protocol('WM_DELETE_WINDOW', onClose)

picoThread.start()
while not picoThread.is_ready():
    pass

window.mainloop()