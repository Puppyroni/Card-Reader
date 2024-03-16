# imports
from tkinter import *
from tkinter import Tk
from Classes.windows.register_window import RegisterWindow
from Classes.windows.login_window import LogInWindow

# Class for the main window
class MainWindow:
    def __init__(self):
        # Create the main window
        self.main_window = Tk() # Create window
        self.main_window.title('Card Reader') # Change Tittle
        self.main_window.iconbitmap('Assets/icons/icon.ico') # Change icon
        self.main_window.configure(bg = '#f0f0f0') # Change the background color
        
        # Configure a welcome text
        self.welcome_lbl = Label(self.main_window, text = 'Card Reader', font = 'Arial 20', bg = '#f0f0f0')
        self.welcome_lbl.grid(row = 0, column = 1, columnspan = 2, pady = 20)
        
        # Configure a button of register
        self.register_btn = Button(self.main_window, text = 'Register', font = 'Arial 14', bg = 'cyan',
                                   command = self.open_window_register) # command missing
        self.register_btn.grid(row = 1, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
        
        # Configure a button of login
        self.login_btn = Button(self.main_window, text = 'Login', font = 'Arial 14', bg = 'cyan',
                                command = self.open_window_login) # command missing
        self.login_btn.grid(row = 2, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
        
        # Configure a button of exit
        self.exit_btn = Button(self.main_window, text = 'Exit', font = 'Arial 14', bg = 'cyan', 
                               command = self.main_window.destroy) # command missing
        self.exit_btn.grid(row = 3, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
        
    def open_window_register(self):
        RegisterWindow()
    
    def open_window_login(self):
        LogInWindow()