import tkinter as tk    


class Example(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent
        self.init_ui()

    def init_ui(self):
        usernameLabel = tk.Label(self, text="Name").grid(row=0, column=0)
        username = tk.StringVar()
        usernameEntry = tk.Entry(self, textvariable=username).grid(row=0, column=1)
        nicknameLabel = tk.Label(self, text="Nickname").grid(row=1, column=0)
        nickname = tk.StringVar()
        nicknameEntry = tk.Entry(self, textvariable=nickname).grid(row=1, column=1)
        emailLabel = tk.Label(self, text="Email").grid(row=2, column=0)
        email = tk.StringVar()
        emailEntry = tk.Entry(self, textvariable=email).grid(row=2, column=1)
        passwordLabel = tk.Label(self,text="Password").grid(row=3, column=0)  
        password = tk.StringVar()
        passwordEntry = tk.Entry(self, textvariable=password, show='*').grid(row=3, column=1)  
        imgLabel = tk.Label(self, text="Img URL").grid(row=4, column=0)
        img = tk.StringVar()
        imgEntry = tk.Entry(self, textvariable=img).grid(row=4, column=1)
        loginButton = tk.Button(self, text="Register").grid(row=5, column=0) 


   

   