# imports
from customtkinter import *
from tkinter import messagebox
import sqlite3
import hashlib
# Windows
from Classes.windows.program_window import ProgramWindow
 
class LogInWindow:
    def __init__(self):
        # Create the login window
        self.login_window = CTkToplevel()
        self.login_window.title('Log In')  # Altere o título
        self.login_window.geometry("250x200")
        self.login_window.resizable(False, False)
       
        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()
        
        # Create the label for login
        self.login_lbl = CTkLabel(self.login_window, text='Log In', fg_color="transparent")
        self.login_lbl.place(relx=0.5, rely=0.1, anchor='center')

        # Create the label and entry field for username
        self.username_lbl = CTkLabel(self.login_window, text='Utilizador', fg_color="transparent")
        self.username_lbl.place(relx=0.3, rely=0.3, anchor='e')
        self.username_entry = CTkEntry(self.login_window)
        self.username_entry.place(relx=0.4, rely=0.3, anchor='w')  # Adjusted relx

        # Create the label and entry field for password
        self.password_lbl = CTkLabel(self.login_window, text='Password', fg_color="transparent")
        self.password_lbl.place(relx=0.3, rely=0.5, anchor='e')
        self.password_entry = CTkEntry(self.login_window, show='*')
        self.password_entry.place(relx=0.4, rely=0.5, anchor='w')  # Adjusted relx

        # Configure the login button
        self.login_btn = CTkButton(self.login_window, text='LogIn', command=self.login_user)
        self.login_btn.place(relx=0.5, rely=0.7, anchor='center')  # Adjusted rely

        # Configure the exit button
        self.exit_btn = CTkButton(self.login_window, text='Sair', command=self.login_window.destroy)
        self.exit_btn.place(relx=0.5, rely=0.9, anchor='center')  # Adjusted rely
        
 
    def login_user(self):
        # Obtenha os dados inseridos
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()
   
        # Consulte o banco de dados para verificar se o nome de usuário inserido está correto
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=?", (entered_username,))
        result = self.cursor.fetchone()
 
        # Verifique se o nome de usuário inserido está presente no banco de dados
        if result:
            # Divida o salt e o hash
            saved_password = str(result[2])
            salt, saved_password_hash = saved_password.split(':')
               
            # Hash a senha inserida usando o mesmo salt
            hashed_password = hashlib.pbkdf2_hmac('sha256', entered_password.encode('utf-8'), bytes.fromhex(salt), 100000).hex()
               
            # Verifique se a senha inserida corresponde ao hash armazenado
            if hashed_password == saved_password_hash:
                self.open_window_program()
                self.login_window.destroy()
                return
 
        # Se as credenciais estiverem incorretas, exiba uma mensagem de erro
        messagebox.showerror('Error', 'Invalid username or password')
 
    def open_window_program(self):
        # Obtenha o nome de usuário inserido na janela de login
        entered_username = self.username_entry.get()
       
        # Passe o nome de usuário para a outra janela
        ProgramWindow(entered_username)
     
    def __del__(self):
        # Feche a conexão com o banco de dados quando o objeto for destruído
        self.conn.close()