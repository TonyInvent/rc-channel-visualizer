# printf("channel_values data:\r\n");
# for (int i = 0; i < CRSF_NUM_CHANNELS; i++)
# {
#     printf("Channel %d: %d\r\n", i, channel_values[i]);
# }
# printf("\r\n");

import tkinter as tk
from tkinter import ttk
import serial
import queue
from threading import Thread
import os

class CRSFGui:
    def __init__(self, master):
        self.master = master
        master.title("CRSF Channel Data")

        self.channel_bars = []
        self.channel_labels = []

        for i in range(16):
            label = ttk.Label(master, text=f"CH{i+1:2d}:")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)

            bar = ttk.Progressbar(master, length=200, maximum=1811-172)
            bar.grid(row=i, column=1, padx=5, pady=2)

            value_label = ttk.Label(master, text="0000")
            value_label.grid(row=i, column=2, sticky="w", padx=5, pady=2)

            self.channel_bars.append(bar)
            self.channel_labels.append(value_label)

        self.data_queue = queue.Queue()
        self.gui_queue = queue.Queue()
        self.channel_values = [0] * 16
        self.uart = None
        self.running = True
        self.init_serial()
        self.serial_thread = Thread(target=self.read_serial, daemon=True)
        self.processing_thread = Thread(target=self.process_data, daemon=True)
        self.serial_thread.start()
        self.processing_thread.start()

        # Lower priority for processing thread
        if hasattr(os, 'nice'):
            os.nice(10)  # Increase nice value (lower priority) on Unix-like systems

        self.master.after(10, self.update_gui)

    def init_serial(self):
        try:
            self.uart = serial.Serial('COM5', 468000, timeout=1)
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.running = False

    def read_serial(self):
        while self.running:
            try:
                line = self.uart.readline().decode('utf-8').strip()
                if line:
                    self.data_queue.put(line)
            except serial.SerialException as e:
                print(f"Serial read error: {e}")
                self.running = False
            except UnicodeDecodeError:
                pass  # Ignore decode errors

    def process_data(self):
        while self.running:
            try:
                line = self.data_queue.get(timeout=1)
                if line.startswith("Channel"):
                    parts = line.split(": ")
                    if len(parts) == 2:
                        channel = int(parts[0].split()[1])
                        value = int(parts[1])
                        self.channel_values[channel] = value
                        self.gui_queue.put((channel, value))
            except queue.Empty:
                pass

    def update_gui(self):
        try:
            while True:
                item = self.gui_queue.get_nowait()
                channel, value = item  # Unpack the tuple here
                self.channel_bars[channel].configure(value=value-172)
                self.channel_labels[channel].configure(text=f"{value:4d}")
        except queue.Empty:
            pass
        finally:
            self.master.after(10, self.update_gui)

    def on_closing(self):
        self.running = False
        if self.uart:
            self.uart.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = CRSFGui(root)
    root.protocol("WM_DELETE_WINDOW", gui.on_closing)
    root.mainloop()
