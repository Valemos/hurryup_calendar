from tkinter import Tk, ttk
import tkinter as tk


from GUI.login_form import FormLogin
from GUI.registration_form import FormRegistration



class AuthorizationWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.geometry("800x500")

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        self.parent['padx'] = 30
        self.parent['pady'] = 30

        self.notebook = ttk.Notebook(self, width=300, height=500)

        login_tab = FormLogin(self.notebook)
        registration_tab = FormRegistration(self.notebook)

        self.notebook.add(login_tab, text="Login")
        self.notebook.add(registration_tab, text="Registration")
        self.notebook.pack()

        self.pack()






if __name__ == '__main__':
    root = Tk()
    root.title('HurryUp')
    ex = AuthorizationWindow(root)
    root.mainloop()