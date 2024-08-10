"""
Description:
  Graphical user interface that displays the official artwork for a
  user-specified Pokémon, which can be set as the desktop background image.

Usage:
  python poke_image_viewer.py
"""

from tkinter import *
from tkinter import ttk
import os
import poke_api
import image_lib
import ctypes

# Get the script and images directory
script_dir = os.path.dirname(os.path.abspath(__file__))
images_dir = os.path.join(script_dir, 'images')

# Create the images directory if it does not exist
if not os.path.exists(images_dir):
    os.makedirs(images_dir)

# Create the main window
root = Tk()
root.title("Pokémon Viewer")
root.geometry('600x600')
root.minsize(500, 500)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Set the icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
root.iconbitmap(os.path.join(script_dir, 'poke_ball.ico'))

# Create frames
frm = ttk.Frame(root)
frm.columnconfigure(0, weight=1)
frm.rowconfigure(0, weight=1)
frm.grid(sticky=NSEW)

# Populate frames with widgets and define event handler functions
lbl_image = ttk.Label(frm, text="Select a Pokémon")
lbl_image.grid(row=0, column=1, padx=(10, 20), pady=(10, 20), sticky=NS)

# Combobox to select Pokémon
poke_list = poke_api.get_pokemon_list()
cbox_poke_sel = ttk.Combobox(frm, values=poke_list, state="readonly")
cbox_poke_sel.grid(row=1, column=1, padx=(10, 20), pady=(10, 20), sticky=NS)

photo = None

def handle_poke_sel(event):
    global photo
    pokemon_name = cbox_poke_sel.get()
    image_path = poke_api.download_pokemon_artwork(pokemon_name, images_dir)
    if image_path:
        photo = PhotoImage(file=image_path)
        lbl_image.config(image=photo, text="")
    else:
        lbl_image.config(text="Failed to load image.", image="")

cbox_poke_sel.bind('<<ComboboxSelected>>', handle_poke_sel)

# Button to set desktop background
def handle_set_desktop():
    global photo
    if photo:
        image_path = os.path.join(images_dir, f"{cbox_poke_sel.get()}.png")
        image_lib.set_desktop_background(image_path)

btn_set_desktop = ttk.Button(frm, text="Set as Desktop Background", command=handle_set_desktop)
btn_set_desktop.grid(row=2, column=1, padx=(10, 20), pady=(10, 20), sticky=NS)

root.mainloop()
