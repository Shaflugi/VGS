from KeyboardListener import listen, handlers
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

bg_color = "#004532"
fg_color = "#00e599"
vgs_data = {}
display_data = []
activation_count = 0
vgs_window = None
labels = []

def vgs_handler(event):
	global activation_count
	global vgs_window

	# Ignore key up	
	if event.event_type == 'key up':
		return

	key_code = event.key_code
	
	if key_code == RIGHT_CTRL:
		activation_count = activation_count + 1
	else:
		activation_count = 0

	print "Current ctrl count: %i" % activation_count
	
	if activation_count >= 2:
		activation_count = 0
		print "VGS activated!"
		spawn_vgs_window()
		
	if vgs_window is not None:
		update_display_data()

def update_display_data():
	for idx,item in enumerate(vgs_data.iterkeys()):
		display_data[idx] = str(item)

def update_vgs_window():
	global vgs_data
	global vgs_window
	
	if vgs_window is None:
		return
	
	vgs_window.after(250, update_vgs_window)
	print "Updating window"

	for idx, _ in enumerate(display_data):
		labels[idx].configure(text=display_data[idx])

def spawn_vgs_window():
	global vgs_window
	vgs_window = tk.Tk()
	
	for i in range(0,15):
		display_data.append(str(""))
		labels.append(tk.Label(vgs_window, text=display_data[i], fg=fg_color,\
			bg=bg_color, justify=tk.LEFT, font="Times 12"))
		labels[i].pack()

	vgs_window.geometry("200x375")
	vgs_window.configure(background=bg_color)
	vgs_window.title("Shazbot!")
	vgs_window.after(1000, update_vgs_window)
	vgs_window.after(500, update_display_data)
	vgs_window.mainloop()

# Read VGS json
fp = open("VGS.json", 'r')
vgs_data = json.load(fp, object_pairs_hook=OrderedDict)
fp.close()

# Add handler to keyboard listener
handlers.append(vgs_handler)
listen()