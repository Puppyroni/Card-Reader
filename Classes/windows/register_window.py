from customtkinter import *
from tkinter import messagebox
import sqlite3
import hashlib
import os

class RegisterWindow:
    def __init__(self, username, job_options):
        self.register_window = CTkToplevel()  # Create CustomTk instance
        self.register_window.title('Registo')  # Change Title
        self.register_window.geometry("250x400") 
        self.register_window.resizable(False, False)
        
        self.job_options = job_options

        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()

        # Create register label
        self.register_lbl = CTkLabel(self.register_window, text='Set Super User', fg_color="transparent")
        self.register_lbl.place(relx=0.5, y=50, anchor='center')

        # Create field for username
        self.username_lbl = CTkLabel(self.register_window, text='Utilizador', fg_color="transparent")
        self.username_lbl.place(relx=0.3, y=100, anchor='e')
        self.username_entry = CTkEntry(self.register_window)
        self.username_entry.place(relx=0.4, y=100, anchor='w')

        # Create field for password
        self.password_lbl = CTkLabel(self.register_window, text='Password', fg_color="transparent")
        self.password_lbl.place(relx=0.3, y=140, anchor='e')
        self.password_entry = CTkEntry(self.register_window, show='*')
        self.password_entry.place(relx=0.4, y=140, anchor='w')

        # Check the query for a SuperUser, Admin or Gerente
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? 
            AND (cargo.cargo_nome='SuperUser' OR cargo.cargo_nome='Admin' OR cargo.cargo_nome='Gerente')
        """, (username,))
        self.result_extra_reg =  self.cursor.fetchone()

        if self.result_extra_reg:
            # Create field for age [Make it not show on first creation of superuser]
            self.age_lbl = CTkLabel(self.register_window, text='Idade', fg_color="transparent")
            self.age_lbl.place(relx=0.3, y=180, anchor='e')
            self.age_entry = CTkEntry(self.register_window)
            self.age_entry.place(relx=0.4, y=180, anchor='w')

            # Create field for address
            self.address_lbl = CTkLabel(self.register_window, text='Morada', fg_color="transparent")
            self.address_lbl.place(relx=0.3, y=220, anchor='e')
            self.address_entry = CTkEntry(self.register_window)
            self.address_entry.place(relx=0.4, y=220, anchor='w')

            # Create field for job
            self.job_lbl = CTkLabel(self.register_window, text='Cargo', fg_color="transparent")
            self.job_lbl.place(relx=0.3, y=260, anchor='e')

            # Dropdown list widget
            self.job_option = CTkOptionMenu(self.register_window, values=job_options)
            self.job_option.place(relx=0.4, y=260, anchor='w')

        # Configure a button of register
        self.register_btn = CTkButton(self.register_window, text='Registar', command=self.register_user)
        self.register_btn.place(relx=0.4, y=300, anchor='center')

        # Configure a button of exit
        self.exit_btn = CTkButton(self.register_window, text='Sair', command=self.register_window.destroy)
        self.exit_btn.place(relx=0.4, y=340, anchor='center')

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
            job_data = self.job_option.get()

        # Generate value of salt
        salt = os.urandom(16)

        # generate a hash sha-256
        password_hash = hashlib.pbkdf2_hmac('sha256', password_data.encode('UTF-8'), salt, 100000)

        # convert password and salt to hexadecimal
        salt_hex = salt.hex()
        password_hash_hex = password_hash.hex()

        # Combine Hashed password with salt
        password_set = f'{salt_hex}:{password_hash_hex}'

        # Check the query for a Super User
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE cargo.cargo_nome='SuperUser'""")
        result = self.cursor.fetchone()

        # Check if SuperUser was inserted
        if result:
            # Query for existing Job
            self.cursor.execute("SELECT id FROM cargo WHERE cargo_nome=?", (job_data,))
            # Retrieve the ID of the existing job
            cargo_id = self.cursor.fetchone()

            # Insert a user
            self.cursor.execute('INSERT INTO funcionarios (nome, password, idade, morada, cargo_id) VALUES (?, ?, ?, ?, ?)',
                                (user_data, password_set, age_data, address_data, cargo_id[0]))
            
            # Message of successful User registry
            messagebox.showinfo('Sucesso', 'O registo foi efectuado com sucesso!')
        else:
            # Insert a user
            self.cursor.execute('INSERT INTO funcionarios (nome, password, idade, morada, cargo_id) VALUES (?, ?, ?, ?, ?)',
                                (user_data, password_set, age_data, address_data, 1))

            # Message of successful SuperUser registry
            messagebox.showinfo('Sucesso', 'SuperUser criado!')

        # Save to the database
        self.conn.commit()

    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()