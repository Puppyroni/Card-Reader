# imports
from tkinter import *
from tkinter import Tk
import sqlite3
import hashlib
import os

class RegisterWindow:
    def __init__(self):
        # Create the register window
        self.register_window = Toplevel() # Create window
        self.register_window.title('Registry') # Change Tittle
        self.register_window.iconbitmap('Assets/icons/icon.ico') # Change icon
        self.register_window.configure(bg = '#f0f0f0') # Change the background color
        
        # Create resgister label
        self.register_lbl = Label(self.register_window, text = 'Registry', font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.register_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        
        # Create field for username
        self.username_lbl = Label(self.register_window, text = 'Username', font = 'Arial 14 bold', bg = '#f0f0f0')
        self.username_lbl.grid(row = 1, column = 0, pady = 20, sticky = 'E')
        self.username_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0')
        self.username_entry.grid(row = 1, column = 1, pady = 20, sticky = 'E')
        
        # Create field for password
        self.Password_lbl = Label(self.register_window, text = 'Password', font = 'Arial 14 bold', bg = '#f0f0f0')
        self.Password_lbl.grid(row = 2, column = 0, pady = 20, sticky = 'E')
        self.Password_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0', show = "*")
        self.Password_entry.grid(row = 2, column = 1, pady = 20, sticky = 'E')
        
        # Configure a button of register
        self.register_btn = Button(self.register_window, text = 'Register', font = 'Arial 14', bg = 'cyan',
                                command = self.register_user)
        self.register_btn.grid(row = 4, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
        
        # Configure a button of exit
        self.exit_btn = Button(self.register_window, text = 'Exit', font = 'Arial 14', bg = 'cyan', 
                               command = self.register_window.destroy)
        self.exit_btn.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
      
      
    def register_user(self):
        # Get inserted data
        user_data = self.username_entry.get()
        password_data = self.Password_entry.get()
        
        # Generate value of salt
        salt = os.urandom(16)
        
        # generate a hash sha-256
        password_hash = hashlib.pbkdf2_hmac('sha256', password_data.encode('UTF-8'), salt, 100000)
        
        # convert password and salt to hexdecimal
        salt_hex = salt.hex()
        password_hash_hex = password_hash.hex()
        
        # Now saving values
        password_saving = f'{salt_hex}:{password_hash_hex}'
        
        # Connect and save to a database
        conn = sqlite3.connect('temp.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO user (user, password) VALUES (?, ?)', (user_data, password_saving))
        conn.commit()     
        conn.close()
        
        # Message of successful registry
        self.message_register_completed = Label(self.register_window, text = 'The Registry was Successful!', fg= 'green')
        self.message_register_completed.grid(row = 3, column = 0, columnspan = 2)
        self.message_register_completed.after(3000, self.register_window.destroy)
        
        