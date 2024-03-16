# imports
from tkinter import *
from tkinter import Tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
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
        
        # Set width and height of the window 
        # Off for now
        #width = self.main_window.winfo_screenwidth()
        #height = self.main_window.winfo_screenheight()
        #alignstr = '%dx%d+0+0' % (width, height)
        #self.main_window.geometry(alignstr)

        # Create Image Background
        # P: Cannat get the image to load idk know why
        try:
            image = Image.open("Assets/image/retrato-de-um-trabalhador-loiro-sorridente-tomando-um-legumes_13339-149292.jpg")
            tk_image = ImageTk.PhotoImage(image)
            image_lbl = Label(self.main_window, image=tk_image)
            image_lbl.place(x=0, y=0)
        except FileNotFoundError:
            print("Arquivo de imagem não encontrado.")
        except TclError:
            print("Erro ao carregar a imagem. Verifique se o formato da imagem é suportado.")
        
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