from tkinter import *
import sqlite3

class DataListWindow:
    def __init__(self):
        # Create the main window
        self.program_window = Toplevel()
        self.program_window.title('Data List')
        self.program_window.iconbitmap('Assets/icons/icon.ico')
        self.program_window.configure(bg='#f0f0f0')
         
        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()