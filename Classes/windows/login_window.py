# imports
from tkinter import *
from PIL import Image, ImageTk
import sqlite3
import hashlib
# Windows
from Classes.windows.program_window import ProgramWindow


class LogInWindow:
    def __init__(self):
        # Create the login window
        self.login_window = Toplevel() # Create window
        self.login_window.title('Log In') # Change Tittle
        self.login_window.iconbitmap('Assets/icons/icon.ico') # Change icon
        self.login_window.configure(bg = '#f0f0f0') # Change the background color
        
        
        # Set the background image
        try:
            pil_image = Image.open("Assets/image/Design sem nome.jpg")
            
            self.image = ImageTk.PhotoImage(pil_image)
            img_lbl = Label(self.login_window, image=self.image)
            img_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Arquivo de imagem não encontrado.")
        except TclError:
            print("Erro ao carregar a imagem. Verifique se o formato da imagem é suportado.")
            
        # Create login label
        self.login_lbl = Label(self.login_window, text='Log In', font='Arial 20', fg='#333333', bg='#f0f0f0')
        self.login_lbl.grid(row=1, column=0, columnspan=2, pady=20, sticky='NSEW')
        
        # Create field for username
        self.username_lbl = Label(self.login_window, text='Username', font='Arial 14 bold', bg='#f0f0f0')
        self.username_lbl.grid(row=2, column=0, pady=20, sticky='E')
        self.username_entry = Entry(self.login_window, font='Arial 14 bold', bg='#f0f0f0')
        self.username_entry.grid(row=2, column=1, pady=20, sticky='E')
        
        # Create field for password
        self.password_lbl = Label(self.login_window, text='Password', font='Arial 14 bold', bg='#f0f0f0')
        self.password_lbl.grid(row=3, column=0, pady=20, sticky='E')
        self.password_entry = Entry(self.login_window, font='Arial 14 bold', bg='#f0f0f0', show='*')
        self.password_entry.grid(row=3, column=1, pady=20, sticky='E')
        
        # Configure a button of login
        self.login_btn = Button(self.login_window, text='LogIn', font='Arial 14', bg='cyan',
                                command=self.login_user)
        self.login_btn.grid(row=4, column=0, columnspan=2, pady=10, sticky='NSEW')
        
        # Configure a button of exit
        self.exit_btn = Button(self.login_window, text='Exit', font='Arial 14', bg='cyan', 
                               command=self.login_window.destroy)
        self.exit_btn.grid(row=5, column=0, columnspan=2, pady=10, sticky='NSEW')
        
        # Centralize all widgets
        self.centralize_widgets()
        
    
    def centralize_widgets(self):
        # Center the login window on the screen
        self.login_window.update_idletasks()
        width = self.login_window.winfo_width()
        height = self.login_window.winfo_height()
        x = (self.login_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.login_window.winfo_screenheight() // 2) - (height // 2)
        self.login_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    
        
    def login_user(self):
        # Get inserted data
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Connect to a database 
        conn = sqlite3.connect('User_Data.db')
        cursor = conn.cursor()
        
        # Query the database to check if the entered username is correct
        cursor.execute("SELECT * FROM funcionarios WHERE nome=?", (entered_username,))
        result = cursor.fetchone()

        # Check if the entered username is present in the database
        if result:
            # Splits Salt and hash
            saved_password = str(result[2])
            salt, saved_password_hash = saved_password.split(':')
                
            # Hash the entered password using the same salt
            hashed_password = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()
                
            # Check if the entered password matches the stored hash
            if hashed_password == saved_password_hash:
            # If credentials are correct, display a success message
                self.message_login_completed = Label(self.login_window, text='The Log In was Successful!', fg='green')
                self.message_login_completed.grid(row=3, column=0, columnspan=2)
                self.message_login_completed.after(1000, self.open_window_program)
                return
        
        # Close the database   
        conn.close()
        
        # If credentials are incorrect, display an error message
        self.message_login_completed = Label(self.login_window, text='Invalid username or password', fg='red')
        self.message_login_completed.grid(row=3, column=0, columnspan=2)
        
        
    def open_window_program(self):
        # Get the username inserted in the login window
        entered_username = self.username_entry.get()
        
        # Pass the username to the other window
        ProgramWindow(entered_username)