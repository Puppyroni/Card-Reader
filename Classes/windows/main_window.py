from customtkinter import *
from customtkinter import CTk
import sqlite3
from Classes.windows.register_window import RegisterWindow
from Classes.windows.login_window import LogInWindow

class MainWindow:
    def __init__(self):
        self.main_window = CTk()
        self.main_window.title('Card Reader')
        self.main_window.geometry("250x200")
        self.main_window.resizable(False, False)

        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute("SELECT * FROM funcionarios WHERE cargo_id=1")
        result = self.cursor.fetchone()

        if not result:
            RegisterWindow('', '')

        self.welcome_lbl = CTkLabel(self.main_window, text='Card Reader', fg_color="transparent")
        self.welcome_lbl.place(relx=0.5, rely=0.3, anchor=CENTER)

        self.login_btn = CTkButton(self.main_window, text='Login', command=self.open_window_login)
        self.login_btn.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.exit_btn = CTkButton(self.main_window, text='Sair', command=self.main_window.destroy)
        self.exit_btn.place(relx=0.5, rely=0.7, anchor=CENTER)
    
    
    def open_window_login(self):
        LogInWindow()
        
    def __del__(self):
        self.conn.close()