# import math
# import time
# import tkinter as  Tkinter  # This is the Tcl/Tk Graphics engine

# # we need a root window object and then a Canvas window object (child)
# # in order to be able to draw points and lines.
# # The Point and Line draw() method will use this canvas.
# #
# # A Canvas Window on which we can draw points, lines, rectangles, etc.
# # See the Tkinter module, Canvas class, for more details.
# # PyScripter may not handle Tkinter well, so to run this example,
# # use the command line:
# #    
# #                   python prog.py
# rootWindow = Tkinter.Tk()
# rootFrame = Tkinter.Frame(rootWindow, width=width, height=height, bg="white")
# rootFrame.pack()
# canvas = Tkinter.Canvas(rootFrame, width=width, height=height, bg="white")
# canvas.config(scrollregion=canvas.bbox(Tkinter.ALL))
# canvas.pack()
import tkinter as tk

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas    
    canvas.configure(scrollregion=canvas.bbox('all'))


root = tk.Tk()
## size of screen 
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
## root size 
root.geometry(f"{width}x{height-100}")
root.geometry("+0+20")
# --- create canvas with scrollbar ---

canvas = tk.Canvas(root)
canvas.pack(expand=True,fill=tk.BOTH)


## create scrool bar 
scrollbary = tk.Scrollbar(canvas, command=canvas.yview)
scrollbarx = tk.Scrollbar(canvas, command=canvas.xview,orient=tk.HORIZONTAL)

scrollbary.pack(side=tk.RIGHT, fill=tk.Y)
scrollbarx.pack(side=tk.BOTTOM, fill=tk.X)
canvas.configure(yscrollcommand = scrollbary.set)
canvas.configure(xscrollcommand = scrollbarx.set)
# update scrollregion after starting 'mainloop'
# when all widgets are in canvas
canvas.bind('<Configure>', on_configure)

# --- put frame in canvas container---

# frame = tk.Frame(canvas)
# canvas.create_window((0,0), window=frame, anchor='nw')
