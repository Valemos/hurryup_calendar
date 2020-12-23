from tkinter import Tk, ttk
import tkinter as tk

from today import Example as Today
from week import Example as Week
from month import Example as Month
from addEvent import Example as AddEvent
from groups import Example as Groups

class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, parent):
        MainWindow.counter+=1
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def __del__(self):  
        MainWindow.counter-=1

    def init_ui(self):
        self.parent['padx'] = 10
        self.parent['pady'] = 10
        self.notebook = ttk.Notebook(self, width=1000, height=700)

        a_tab = Today(self.notebook)
        b_tab = Week(self.notebook)
        c_tab = Month(self.notebook)
        d_tab = AddEvent(self.notebook)
        e_tab = Groups(self.notebook)
        self.notebook.add(a_tab, text="Today")
        self.notebook.add(b_tab, text="Week")
        self.notebook.add(c_tab, text="Month")
        self.notebook.add(d_tab,text="Add Event")
        self.notebook.add(e_tab,text="Groups")

        self.notebook.pack()

        self.pack()