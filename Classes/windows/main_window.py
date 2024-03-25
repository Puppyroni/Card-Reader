# imports
from tkinter import *
from tkinter import Tk
from PIL import Image, ImageTk
import sqlite3
# Windows
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
        

        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()
        
        # Check the quary for a SuperUser
        self.cursor.execute("SELECT * FROM funcionarios WHERE cargo_id=1")
        result = self.cursor.fetchone()
        
        # Check if SuperUser was not created
        if not result:
            RegisterWindow('', '')
        
        # Set the background image
        try:
            pil_image = Image.open('Assets/image/Design sem nome.jpg')
            
            self.image = ImageTk.PhotoImage(pil_image)
            img_lbl = Label(self.main_window, image=self.image)
            img_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print('Arquivo de imagem não encontrado.')
        except TclError:
            print('Erro ao carregar a imagem. Verifique se o formato da imagem é suportado.')
            
        # Set window size to match image size
        self.main_window.geometry(f"{pil_image.width}x{pil_image.height}")
       
        
        # Configure a welcome text
        self.welcome_lbl = Label(self.main_window, text = 'Card Reader', font = 'Arial 20', bg = '#f0f0f0')
        self.welcome_lbl.pack(pady=(50, 10))  # Ajuste do espaçamento superior e inferior

        # Configure a button of login
        self.login_btn = Button(self.main_window, text = 'Login', font = 'Arial 14', bg = 'cyan', command=self.open_window_login)
        self.login_btn.pack(pady=(10, 5))  # Ajuste do espaçamento superior e inferior

        # Configure a button of exit
        self.exit_btn = Button(self.main_window, text = 'Exit', font = 'Arial 14', bg = 'cyan', command=self.main_window.destroy)
        self.exit_btn.pack(pady=(5, 50))  # Ajuste do espaçamento superior e inferio
        
    
    def open_window_login(self):
        LogInWindow()
        
    
    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()