# imports
from tkinter import *
from tkinter import Tk
from tkinter import PhotoImage
from PIL import Image, ImageTk

# Placeholder so that the window works
class LogInWindow:
    def __init__(self):
        # Create the login window
        self.login_window = Toplevel() # Create window
        self.login_window.title('Log In') # Change Tittle
        self.login_window.iconbitmap('Assets/icons/icon.ico') # Change icon
        self.login_window.configure(bg = '#f0f0f0') # Change the background color
        
        # Set the background image
        try:
            pil_image = Image.open("Assets/image/MainBG.jpg") # Using same as the main window as placeholder for now
            
            self.image = ImageTk.PhotoImage(pil_image)
            img_lbl = Label(self.login_window, image=self.image)
            img_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Arquivo de imagem não encontrado.")
        except TclError:
            print("Erro ao carregar a imagem. Verifique se o formato da imagem é suportado.")
            
        # Set and Lock window size to match image size
        self.login_window.geometry(f"{pil_image.width}x{pil_image.height}")
        self.login_window.minsize(pil_image.width, pil_image.height)
        self.login_window.maxsize(pil_image.width, pil_image.height)
        
        # Create login label
        self.register_lbl = Label(self.login_window, text = 'Log In', font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.register_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        
        # Create field for username
        self.username_lbl = Label(self.login_window, text = 'Username', font = 'Arial 14 bold', bg = '#f0f0f0')
        self.username_lbl.grid(row = 1, column = 0, pady = 20, sticky = 'E')
        self.username_entry = Entry(self.login_window, font = 'Arial 14 bold', bg = '#f0f0f0')
        self.username_entry.grid(row = 1, column = 1, pady = 20, sticky = 'E')
        
        # Create field for password
        self.Password_lbl = Label(self.login_window, text = 'Password', font = 'Arial 14 bold', bg = '#f0f0f0')
        self.Password_lbl.grid(row = 2, column = 0, pady = 20, sticky = 'E')
        self.Password_entry = Entry(self.login_window, font = 'Arial 14 bold', bg = '#f0f0f0', show = "*")
        self.Password_entry.grid(row = 2, column = 1, pady = 20, sticky = 'E')
        
        # Configure a button of login
        self.register_btn = Button(self.login_window, text = 'LogIn', font = 'Arial 14', bg = 'cyan',
                                command = self.login_user)
        self.register_btn.grid(row = 4, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
        
        # Configure a button of exit
        self.exit_btn = Button(self.login_window, text = 'Exit', font = 'Arial 14', bg = 'cyan', 
                               command = self.login_window.destroy)
        self.exit_btn.grid(row = 5, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
    
        
    def login_user(self):
        self.message_login_completed = Label(self.login_window, text = 'The Log In was Successful!', fg= 'green')
        self.message_login_completed.grid(row = 3, column = 0, columnspan = 2)