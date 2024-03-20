# imports
from tkinter import *
from PIL import Image, ImageTk
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
        
        
        # Set the background image
        try:
            pil_image = Image.open("Assets/image/RegisterBG.jpg")
            
            self.image = ImageTk.PhotoImage(pil_image)
            img_lbl = Label(self.register_window, image=self.image)
            img_lbl.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError:
            print("Arquivo de imagem não encontrado.")
        except TclError:
            print("Erro ao carregar a imagem. Verifique se o formato da imagem é suportado.")
            
        # Set and Lock window size to match image size
        self.register_window.geometry(f"{pil_image.width}x{pil_image.height}")
        self.register_window.minsize(pil_image.width, pil_image.height)
        self.register_window.maxsize(pil_image.width, pil_image.height)
        
        # Create resgister label
        self.register_lbl = Label(self.register_window, text = 'Set Super User', font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.register_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        
        # Create field for username
        self.username_lbl = Label(self.register_window, text = 'Username', font = 'Arial 14 bold', bg = '#f0f0f0')
        self.username_lbl.grid(row = 1, column = 0, pady = 20, sticky = 'E')
        self.username_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0')
        self.username_entry.grid(row = 1, column = 1, pady = 20, sticky = 'E')
        
        # Create field for password
        self.password_lbl = Label(self.register_window, text = 'Password', font = 'Arial 14 bold', bg = '#f0f0f0')
        self.password_lbl.grid(row = 2, column = 0, pady = 20, sticky = 'E')
        self.password_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0', show = "*")
        self.password_entry.grid(row = 2, column = 1, pady = 20, sticky = 'E')
        
        # Connect to a database
        conn = sqlite3.connect('User_Data.db')
        cursor = conn.cursor()
        
        # Get Inserted Username
        username = self.username_entry.get()
        
        # Check the quary for a SuperUser, Admin or Chief
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='SuperUser' or cargo='Admin' or cargo='Chefe'", 
                       (username,))
        self.result_extra_reg = cursor.fetchone()
        
        if self.result_extra_reg:
            # Create resgister label
            self.register_lbl = Label(self.register_window, text = 'Registry', font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
            self.register_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
            
            # Create field for age [Make it not show on first creation of superuser]
            self.age_lbl = Label(self.register_window, text = 'Age', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.age_lbl.grid(row = 3, column = 0, pady = 20, sticky = 'E')
            self.age_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0', show = "*")
            self.age_entry.grid(row = 3, column = 1, pady = 20, sticky = 'E')
                
            # Create field for address
            self.address_lbl = Label(self.register_window, text = 'Address', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.address_lbl.grid(row = 4, column = 0, pady = 20, sticky = 'E')
            self.address_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0', show = "*")
            self.address_entry.grid(row = 4, column = 1, pady = 20, sticky = 'E')
            
            # Create field for job
            self.job_lbl = Label(self.register_window, text = 'Job', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.job_lbl.grid(row = 5, column = 0, pady = 20, sticky = 'E')
            self.job_entry = Entry(self.register_window, font = 'Arial 14 bold', bg = '#f0f0f0', show = "*")
            self.job_entry.grid(row = 5, column = 1, pady = 20, sticky = 'E')
        
        # Check the quary for a SuperUser
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='SuperUser'", (username,))
        result_superuser = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_superuser:
            # Allow ability to Create Admins, Chiefs and Workers
            self.temp_lbl = Label(self.register_window, text = 'Can create Admin, Workers and Chiefs', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 5, column = 2, pady = 20, sticky = 'E')
            
        # Check the quary for a Admin 
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='Admin'", (username,))
        result_admin = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_admin:
            # Allow ability to Create workers
            self.temp_lbl = Label(self.register_window, text = 'Can create Workers and Chiefs', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 5, column = 2, pady = 20, sticky = 'E')
        
        # Check the quary for a Chefe 
        cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='Chefe'", (username,))
        result_chief = cursor.fetchone()
        
        # Check if the entered username is a SuperUser or a Admin
        if result_chief:
            # Allow ability to Create workers
            self.temp_lbl = Label(self.register_window, text = 'Can create Workers but not other Chiefs', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 5, column = 2, pady = 20, sticky = 'E')
            
        # save and close the database
        conn.commit()     
        conn.close()
            
        # Configure a button of register
        self.register_btn = Button(self.register_window, text = 'Register', font = 'Arial 14', bg = 'cyan',
                                command = self.register_user)
        self.register_btn.grid(row = 7, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
        
        # Configure a button of exit
        self.exit_btn = Button(self.register_window, text = 'Exit', font = 'Arial 14', bg = 'cyan', 
                               command = self.register_window.destroy)
        self.exit_btn.grid(row = 8, column = 1, columnspan = 2, padx = 20, pady = 10, sticky = 'NSEW')
      
      
    def register_user(self):
        # Get inserted data
        user_data = self.username_entry.get()
        password_data = self.password_entry.get()
        age_data = ''
        address_data = ''
        job_data = ''
        
        if self.result_extra_reg:
            age_data = self.age_entry.get()
            address_data = self.address_entry.get()
            job_data = self.job_entry.get()
        
        # Generate value of salt
        salt = os.urandom(16)
        
        # generate a hash sha-256
        password_hash = hashlib.pbkdf2_hmac('sha256', password_data.encode('UTF-8'), salt, 100000)
        
        # convert password and salt to hexdecimal
        salt_hex = salt.hex()
        password_hash_hex = password_hash.hex()
        
        # Now saving values
        password_saving = f'{salt_hex}:{password_hash_hex}'
    
        
        # Connect to a database
        conn = sqlite3.connect('User_Data.db')
        cursor = conn.cursor()
        # Check the quary for a Super User
        cursor.execute("SELECT * FROM funcionarios WHERE cargo='SuperUser'")
        result = cursor.fetchone()
        
        # Check if SuperUser was inserted
        if result:
            # Insert a user
            cursor.execute('INSERT INTO funcionarios (nome, password, idade, morada, cargo) VALUES (?, ?, ?, ?, ?)', 
                           (user_data, password_saving, age_data, address_data, job_data))
        else:
            # Insert a superuser
            cursor.execute('INSERT INTO funcionarios (nome, password, idade, morada, cargo) VALUES (?, ?, ?, ?, ?)', 
                           (user_data, password_saving, age_data, address_data, 'SuperUser'))
            
            # Message of successful registry
            self.message_register_completed = Label(self.register_window, text = 'SuperUser!', fg= 'green')
            self.message_register_completed.grid(row = 9, column = 0, columnspan = 2)
        
        # save and close the database
        conn.commit()     
        conn.close()
        
        # Message of successful registry
        self.message_register_completed = Label(self.register_window, text = 'The Registry was Successful!', fg= 'green')
        self.message_register_completed.grid(row = 6, column = 0, columnspan = 2)
        self.message_register_completed.after(3000, self.register_window.destroy)
        
        