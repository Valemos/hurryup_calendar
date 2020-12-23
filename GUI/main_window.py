from tkinter import Tk, ttk
import tkinter as tk

from GUI.today_view import TodayView
from GUI.week_view import WeekView
from GUI.month_view import MonthView
from GUI.add_event import FormAddEvent
from GUI.groups_list import GroupsList


class MainWindow(tk.Frame):
    counter = 0
    def __init__(self, parent):
        MainWindow.counter += 1
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def __del__(self):  
        MainWindow.counter -= 1

    def init_ui(self):
        self.parent['padx'] = 10
        self.parent['pady'] = 10
        self.notebook = ttk.Notebook(self, width=1000, height=700)

        self.today_view = TodayView(self.notebook)
        self.week_view = WeekView(self.notebook)
        self.month_view = MonthView(self.notebook)
        self.form_add_event = FormAddEvent(self.notebook)
        self.event_groups_list = GroupsList(self.notebook)
        self.notebook.add(self.today_view, text="Today")
        self.notebook.add(self.week_view, text="Week")
        self.notebook.add(self.month_view, text="Month View")
        self.notebook.add(self.form_add_event, text="Add Event")
        self.notebook.add(self.event_groups_list, text="Groups List")

        self.notebook.pack()
        self.pack()