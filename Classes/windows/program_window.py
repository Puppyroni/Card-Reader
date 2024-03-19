# imports
from tkinter import *
import sqlite3
# Windows
from Classes.windows.register_window import RegisterWindow


class ProgramWindow:
    def __init__(self, username):
        # Create the main window
        self.program_window = Toplevel() # Create window
        self.program_window.title('Program') # Change Tittle
        self.program_window.iconbitmap('Assets/icons/icon.ico') # Change icon
        self.program_window.configure(bg = '#f0f0f0') # Change the background color
        
        # Connect to a database
        conn = sqlite3.connect('User_Data.db')
        cursor = conn.cursor()
        # Check the quary for a inserted username from login
        cursor.execute("SELECT * FROM funcionarios WHERE nome=?", (username,))
        result_user = cursor.fetchone()
        
        # Create info field
        self.name_lbl = Label(self.program_window, text = result_user[1], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.name_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        self.job_lbl = Label(self.program_window, text = result_user[5], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.job_lbl.grid(row = 1, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        
        # Check the quary for a SuperUser or Admin
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='SuperUser' or cargo='Admin' or cargo='Chefe'", 
                       (username,))
        result_job = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_job:
            # Configure a button of register
            self.register_btn = Button(self.program_window, text = 'Register', font = 'Arial 14', bg = 'cyan',
                                    command = self.open_window_register) # command missing
            self.register_btn.grid(row = 2, column = 1, columnspan = 2, padx = 20, pady = 10)
        
        # Connect to a database 
        conn = sqlite3.connect('User_Data.db')
        cursor = conn.cursor()
        
        
    def open_window_register(self):
        RegisterWindow()