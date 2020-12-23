import tkinter as tk    


class GroupsList(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.pack(fill=tk.BOTH, expand=1)

        self.list_box_main = tk.Listbox(self, width=500)
        self.var_group_list = tk.StringVar()
        self.label = tk.Label(self, text=0, textvariable=self.var_group_list)
        self.label.pack()

        self.pack()

    def add_group(self, group):
        self.list_box_main.insert(tk.END, group)
        self.list_box_main.bind("<<ListboxSelect>>", self.on_select)
        self.list_box_main.pack(pady=15)

    def on_select(self, val):
        sender = val.widget
        idx = sender.curselection()
        value = sender.get(idx)

        self.var_group_list.set(value)