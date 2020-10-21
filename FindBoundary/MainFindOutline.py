from tkinter import Tk
from tkinter.filedialog import askopenfilename
from Outline import Outline
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
Outline=Outline(filename)
Outline.FindOutline()

