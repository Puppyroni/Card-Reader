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
        self.age_lbl = Label(self.program_window, text = result_user[3], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.age_lbl.grid(row = 1, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        self.address_lbl = Label(self.program_window, text = result_user[4], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.address_lbl.grid(row = 2, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        self.job_lbl = Label(self.program_window, text = result_user[5], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.job_lbl.grid(row = 3, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        
        # Check the quary for a SuperUser, Admin or Chief
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='SuperUser' or cargo='Admin' or cargo='Chefe'", 
                       (username,))
        result_job = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_job:
            # Configure a button of register
            self.register_btn = Button(self.program_window, text = 'Register', font = 'Arial 14', bg = 'cyan',
                                    command = self.open_window_register) # command missing
            self.register_btn.grid(row = 2, column = 1, columnspan = 2, padx = 20, pady = 10)
            
                # Check the quary for a SuperUser
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='SuperUser'", (username,))
        result_superuser = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_superuser:
            # Allow ability to Create Admins, Chiefs and Workers
            self.temp_lbl = Label(self.program_window, text = 'Can create Admin, Workers and Chiefs', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 5, column = 2, pady = 20, sticky = 'E')
            
        # Check the quary for a Admin 
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='Admin'", (username,))
        result_admin = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_admin:
            # Allow ability to Create workers
            self.temp_lbl = Label(self.program_window, text = 'Can create Workers and Chiefs', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 5, column = 2, pady = 20, sticky = 'E')
        
        # Check the quary for a Chefe 
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='Chefe'", (username,))
        result_chief = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_chief:
            # Allow ability to Create workers
            self.temp_lbl = Label(self.program_window, text = 'Can create Workers but not other Chiefs', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 5, column = 2, pady = 20, sticky = 'E')
        
        # Connect to a database 
        conn = sqlite3.connect('User_Data.db')
        cursor = conn.cursor()
        
        
    def open_window_register(self):
        # Get the username inserted in the login window
        username = self.name_lbl.cget('text')
        
        RegisterWindow(username)