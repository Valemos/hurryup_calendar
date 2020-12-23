import tkinter as tk    
from mainWindow import MainWindow as mainWindow


class Example(tk.Frame):

    
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.init_ui()

    def init_ui(self):
        usernameLabel = tk.Label(self, text="Name").grid(row=0, column=0)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username).grid(row=0, column=1)
        passwordLabel = tk.Label(self,text="Password").grid(row=3, column=0)  
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=password, show='*').grid(row=3, column=1)  
        loginButton = tk.Button(self, text="Login", command= lambda u=username,p=password:self.validateLogin(username,password)).grid(row=4, column=0) 

    def startMainWindow(self):
        if mainWindow.counter == 0:
            newWindow = tk.Toplevel(self)
            window = mainWindow(newWindow)

    def validateLogin(self,username, password):
        print("username entered :", username.get())
        print("password entered :", password.get())
        self.startMainWindow()
    
    