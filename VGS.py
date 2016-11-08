import KeyboardListener
import Tkinter as tk
import json
from Tkinter import StringVar
from time import sleep
from collections import OrderedDict

RIGHT_CTRL = 163
"""
v: 86
g: 71
s: 83
"""


class VGS:

    def __init__(self):
        self._activation_count = 0
        self._window = None
        self._labels = []
        self._vgs_data = {}
        self._display_data = []
        self._bg_color = "#004532"
        self._fg_color = "#00e599"

        # Read VGS json
        fp = open("VGS.json", 'r')
        self._vgs_data = json.load(fp, object_pairs_hook=OrderedDict)
        fp.close()

    def begin_listening(self):
        # Add handler to keyboard listener
        KeyboardListener.handlers.append(self.keyboard_handler)
        KeyboardListener.listen()

    def keyboard_handler(self, event):
        # Ignore key up
        if event.event_type == 'key up':
            return

        key_code = event.key_code

        if key_code == RIGHT_CTRL:
            self._activation_count += 1
        else:
            self._activation_count = 0

        print "Current ctrl count: %i" % self._activation_count

        if self._activation_count >= 2:
            activation_count = 0
            print "VGS activated!"
            self.spawn_window()

        if self._window is not None:
            self.update_display_data()

    def update_display_data(self):
        for idx,item in enumerate(self._vgs_data.iterkeys()):
            self._display_data[idx] = str(item)

    def update_window(self):
        if self._window is None:
            return

        self._window.after(250, self.update_window)
        print "Updating window"

        for idx, _ in enumerate(self._display_data):
            self._labels[idx].configure(text=self._display_data[idx])

    def spawn_window(self):
        self._window = tk.Tk()

        for i in range(0,15):
            self._display_data.append(str(""))
            self._labels.append(tk.Label(self._window, text=self._display_data[i],
                                         fg=self._fg_color, bg=self._bg_color, justify=tk.LEFT,
                                         font="Times 12"))
            self._labels[i].pack()

        self._window.geometry("200x375")
        self._window.configure(background=self._bg_color)
        self._window.title("Shazbot!")
        self._window.after(1000, self.update_window)
        self._window.after(500, self.update_display_data)
        self._window.mainloop()

if __name__ == '__main__':
    vgs = VGS()
    vgs.begin_listening()
