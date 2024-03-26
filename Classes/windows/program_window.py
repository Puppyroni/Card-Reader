from customtkinter import *
import sqlite3
from datetime import datetime, timedelta
from Classes.windows.register_window import RegisterWindow
from Classes.windows.data_list_window import DataListWindow
 
class ProgramWindow:
    def __init__(self, username):
        self.username = username  # Store the username as an instance attribute
       
        # Create the main window
        self.program_window = CTkToplevel()
        self.program_window.title('Programa')
        self.program_window.resizable(False, False)
         
        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()
       
        # Check the query for an inserted username from login
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=?", (username,))
        result_user = self.cursor.fetchone()
       
        # Create Name label
        self.name_lbl = CTkLabel(self.program_window, text=result_user[1], fg_color="transparent")
        self.name_lbl.grid(row=0, column=0, columnspan=4, pady=20, sticky='NSEW')
       
        # Check the query for a SuperUser, Admin, or Chief
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=?
        """, (username,))
        result_user_job = self.cursor.fetchone()
       
        # Create job label
        self.job_lbl = CTkLabel(self.program_window, text=result_user_job[6], fg_color="transparent")
        self.job_lbl.grid(row=1, column=0, columnspan=4, pady=20, sticky='NSEW')
       
        # Check the query for a SuperUser, Admin, or Chief
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=?
            AND (cargo.cargo_nome='SuperUser' OR cargo.cargo_nome='Admin' OR cargo.cargo_nome='Gerente')
        """, (username,))
        result_job = self.cursor.fetchone()
 
        # Check if the entered username is a SuperUser
        if result_job:
            # Configure a button of register
            self.register_btn = CTkButton(self.program_window, text='Registar', command=self.open_window_register)
            self.register_btn.grid(row=17, column=2, columnspan=2, padx=20, pady=10)
           
            # Configure a button of worker's schedule
            self.Schedule_btn = CTkButton(self.program_window, text='Horários', command=self.open_window_data_list)
            self.Schedule_btn.grid(row=18, column=2, columnspan=2, padx=20, pady=10)
           
        # Check the quary for a SuperUser
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? AND cargo.cargo_nome='SuperUser'
        """, (username,))
        result_superuser = self.cursor.fetchone()
       
       
        # Options for the dropdown list
        self.job_options = []
       
        if result_superuser:
            # Fetch cargo names from the database
            self.cursor.execute("SELECT cargo_nome FROM cargo")
            cargo_names = self.cursor.fetchall()
            
            # Extend job_options with the fetched cargo names
            self.job_options.extend(cargo[0] for cargo in cargo_names)
           
        # Check the quary for a Admin
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? AND cargo.cargo_nome='Admin'
        """, (username,))
        result_admin = self.cursor.fetchone()
       
        # Check if the entered username is a a Admin
        if result_admin:
            # Fetch cargo names from the database
            self.cursor.execute("SELECT cargo_nome FROM cargo WHERE NOT cargo_nome='SuperUser'")
            cargo_names = self.cursor.fetchall()
            
            # Extend job_options with the fetched cargo names
            self.job_options.extend(cargo[0] for cargo in cargo_names)
           
        # Check the quary for a Gerente
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? AND cargo.cargo_nome='Gerente'
        """, (username,))
        result_maneger = self.cursor.fetchone()
       
        # Check if the entered username is a Chefe
        if result_maneger:
            # Fetch cargo names from the database
            self.cursor.execute("SELECT cargo_nome FROM cargo WHERE NOT cargo_nome='SuperUser' AND NOT cargo_nome='Admin'")
            cargo_names = self.cursor.fetchall()
            
            # Extend job_options with the fetched cargo names
            self.job_options.extend(cargo[0] for cargo in cargo_names)
           
        self.enter_btn = CTkButton(self.program_window, text='Entrar', command=self.enter_action)
        self.enter_btn.grid(row=2, column=0, padx=20, pady=10, sticky='NSEW')

        self.pause_btn = CTkButton(self.program_window, text='Pausa', command=self.pause_action)
        self.pause_btn.grid(row=2, column=1, padx=20, pady=10, sticky='NSEW')

        self.resume_btn = CTkButton(self.program_window, text='Voltar da Pausa', command=self.resume_action)
        self.resume_btn.grid(row=2, column=2, padx=20, pady=10, sticky='NSEW')

        self.exit_btn = CTkButton(self.program_window, text='Sair do Trabalho', command=self.exit_action)
        self.exit_btn.grid(row=2, column=3, padx=20, pady=10, sticky='NSEW')
 
        # Configure labels with improved design
        self.entry_time_lbl = CTkLabel(self.program_window, text='', fg_color="transparent")
        self.entry_time_lbl.grid(row=3, column=0, columnspan=4, padx=20, pady=10, sticky='NSEW')

        # Configure Clock label
        self.clock_lbl = CTkLabel(self.program_window, text='', fg_color="transparent")
        self.clock_lbl.grid(row=4, column=0, columnspan=4, pady=10, sticky='NSEW')
           
        # Update clock label every second
        self.update_clock()
       
       
    def open_window_register(self):
        # Get the username label text in the login window
        username = self.name_lbl.cget('text')
       
        # Pass the username and job options to the other window
        RegisterWindow(username, self.job_options)
       
       
    def open_window_data_list(self):
        # Get the username label text in the login window
        username = self.name_lbl.cget('text')
        job = self.job_lbl.cget('text')
       
        # Pass the username to the other window
        DataListWindow(username, job)
 
 
    def enter_action(self):
        # Get current time
        current_time = datetime.now().strftime('%H:%M:%S')
 
        # Check if an entry already exists
        self.cursor.execute("SELECT id FROM picagem_entrada WHERE id_funcionario = ? AND picagem_data = ?",
                            (self.get_user_id(), datetime.now().date()))
        existing_entry = self.cursor.fetchone()
       
        # Check if the data does not exists
        if not existing_entry:
            # Insert entry time into the database
            self.cursor.execute("INSERT INTO picagem_entrada (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                                (self.get_user_id(), datetime.now().date(), current_time))
           
            # Save to the database
            self.conn.commit()
       
        # Check if an exit record already exists
        self.cursor.execute("SELECT id FROM picagem_saida WHERE id_funcionario = ? AND picagem_data = ?",
                            (self.get_user_id(), datetime.now().date()))
        existing_exit = self.cursor.fetchone()
       
        # If an exit record exists, delete it and insert a new one
        if existing_exit:
            # Delete exit time from the database
            self.cursor.execute("DELETE FROM picagem_saida WHERE id = ?", (existing_exit[0],))
           
            # Save to the database
            self.conn.commit()
       
 
        # Display entry time and message
        self.entry_time_lbl.configure(text=f'Entrada: {current_time}\nBom trabalho!')
 
       
       
    def pause_action(self):
        self.pause_start_time = datetime.now()
 
        # Exibir mensagem para o funcionário
        current_time = self.pause_start_time.strftime('%H:%M:%S')
        self.entry_time_lbl.configure(text=f'Pausa iniciada: {current_time}\nBom almoço!')
       
        # Insert pause start time into the database
        self.cursor.execute("INSERT INTO picagem_entrada_pausa (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                            (self.get_user_id(), datetime.now().date(), current_time))
       
        # Save to the database
        self.conn.commit()
       
   
    def resume_action(self):
        # Calculate the duraction of the break
        pause_duration = datetime.now() - self.pause_start_time
        pause_duration_str = str(timedelta(seconds=pause_duration.seconds))
 
        # Exibir mensagem para o funcionário
        current_time = datetime.now().strftime('%H:%M:%S')
        self.entry_time_lbl.configure(text=f'Voltou da Pausa: {current_time}\nDuração da Pausa: {pause_duration_str}')
       
        # Insert pause exit time into the database
        self.cursor.execute("INSERT INTO picagem_saida_pausa (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                            (self.get_user_id(), datetime.now().date(), current_time))
       
        # Save to the database
        self.conn.commit()
       
   
    def exit_action(self):
        # Get current time
        current_time = datetime.now().strftime('%H:%M:%S')
 
        # Check if an exit record already exists
        self.cursor.execute("SELECT id FROM picagem_saida WHERE id_funcionario = ? AND picagem_data = ?",
                            (self.get_user_id(), datetime.now().date()))
        existing_exit = self.cursor.fetchone()
       
        # Checks if exit time does not exists
        if not existing_exit:
            # Insert exit time into the database
            self.cursor.execute("INSERT INTO picagem_saida (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                                (self.get_user_id(), datetime.now().date(), current_time))
            # Save to the database
            self.conn.commit()
 
        # Display exit time and message
        self.entry_time_lbl.configure(text=f'Saida: {current_time}\nBom trabalho!')
 
 
   
    def get_user_id(self):
        # Retrieve user ID from the database based on the username
        self.cursor.execute("SELECT id FROM funcionarios WHERE nome=?", (self.username,))
        user_id = self.cursor.fetchone()
       
        # Check for the username
        return user_id[0] if user_id else None
   
   
    def update_clock(self):
        # Get current system time
        current_time = datetime.now().strftime('%H:%M:%S')
    
        # Update clock label
        self.clock_lbl.configure(text=f'Hora atual: {current_time}')
    
        # Schedule next update after 1000ms (1 second)
        self.program_window.after(1000, self.update_clock)
   
   
    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()