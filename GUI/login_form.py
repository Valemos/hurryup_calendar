import tkinter as tk    
from GUI.main_window import MainWindow as mainWindow


class FormLogin(tk.Frame):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        usernameLabel = tk.Label(self, text="Name").grid(row=0, column=0)
        self.var_username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=self.var_username).grid(row=0, column=1)
        passwordLabel = tk.Label(self, text="Password").grid(row=3, column=0)
        self.var_password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=self.var_username, show='*').grid(row=3, column=1)
        loginButton = tk.Button(self, text="Login", command=self.validateLogin).grid(row=4, column=0)

    def start_main_window(self):
        if mainWindow.counter == 0:
            newWindow = tk.Toplevel(self)
            window = mainWindow(newWindow)

    def validateLogin(self):
        print("username entered :", self.var_username.get())
        print("password entered :", self.var_username.get())
        self.start_main_window()
    
    