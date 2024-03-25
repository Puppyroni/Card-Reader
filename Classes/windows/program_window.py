from tkinter import *
from datetime import datetime, timedelta
import sqlite3
from Classes.windows.register_window import RegisterWindow
from Classes.windows.data_list_window import DataListWindow

class ProgramWindow:
    def __init__(self, username):
        self.username = username  # Store the username as an instance attribute
        
        # Create the main window
        self.program_window = Toplevel()
        self.program_window.title('Program')
        self.program_window.iconbitmap('Assets/icons/icon.ico')
        self.program_window.configure(bg='#f0f0f0')
         
        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()
        
        # Check the query for an inserted username from login
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=?", (username,))
        result_user = self.cursor.fetchone()
        
        # Create info field
        # Name
        self.name_lbl = Label(self.program_window, text = result_user[1], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.name_lbl.grid(row = 0, column = 0, columnspan = 2, pady = 20, sticky = 'NSEW')
        # Job
        self.job_lbl = Label(self.program_window, text = result_user[5], font = 'Arial 20', fg = '#333333', bg = '#f0f0f0')
        self.job_lbl.grid(row = 0, column = 2, columnspan = 2, pady = 20, sticky = 'NSEW')
        
        # Check the query for a SuperUser, Admin, or Chief
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? 
            AND (cargo.cargo_nome='SuperUser' OR cargo.cargo_nome='Admin' OR cargo.cargo_nome='Chefe')
        """, (username,))
        result_job = self.cursor.fetchone()

        # Check if the entered username is a SuperUser
        if result_job:
            # Configure a button of register
            self.register_btn = Button(self.program_window, text = 'Register', font = 'Arial 14', bg = 'cyan', command = self.open_window_register)
            self.register_btn.grid(row = 4, column = 2, columnspan = 2, padx = 20, pady = 10)
            
            # Configure a button of worker's schedule TEMP: for now uses register Button
            self.Schedule_btn = Button(self.program_window, text = 'Schedules', font = 'Arial 14', bg = 'cyan', command = self.open_window_data_list)
            self.Schedule_btn.grid(row = 5, column = 2, columnspan = 2, padx = 20, pady = 10)
            
        # Check the quary for a SuperUser
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? AND cargo.cargo_nome='SuperUser'
        """, (username,))
        result_superuser = self.cursor.fetchone()
        
        
        # Options for the dropdown list
        self.job_options = []
        
        # Check if the entered username is a SuperUser
        if result_superuser:
            # Allow ability to Create Admins, Chefes and Workers
            # Append SuperUser options to job_options
            self.job_options.extend(['Admin', 'Gerente', 'Temp'])
            
        # Check the quary for a Admin 
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? AND cargo.cargo_nome='Admin'
        """, (username,))
        result_admin = self.cursor.fetchone()
        
        # Check if the entered username is a a Admin
        if result_admin:
            # Allow ability to Create workers and Chefes
            # Append Admin options to job_options
            self.job_options.extend(['Gerente', 'Temp'])
            
        # Check the quary for a Gerente 
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? AND cargo.cargo_nome='Gerente'
        """, (username,))
        result_maneger = self.cursor.fetchone()
        
        # Check if the entered username is a Chefe
        if result_maneger:
            # Allow ability to Create workers
            # Append Chefe options to job_options
            self.job_options.extend(['temp'])
            
        # Configure buttons for actions
        self.enter_btn = Button(self.program_window, text='Entrar', font='Arial 14', bg='cyan', command=self.enter_action)
        self.enter_btn.grid(row=5, column=0, padx=20, pady=10)
            
        # Create label for displaying entry time
        self.entry_time_lbl = Label(self.program_window, text='', font='Arial 14', bg='#f0f0f0')
        self.entry_time_lbl.grid(row=5, column=1, padx=20, pady=10)
        
        # Create label for displaying entry break time    
        self.pause_btn = Button(self.program_window, text='Pausa', font='Arial 14', bg='cyan', command=self.pause_action)
        self.pause_btn.grid(row=6, column=0, padx=20, pady=10)
        
        # Create label for displaying exit break time   
        self.resume_btn = Button(self.program_window, text='Voltar da Pausa', font='Arial 14', bg='cyan', command=self.resume_action)
        self.resume_btn.grid(row=6, column=1, padx=20, pady=10)
        
        # Create label for displaying exit time     
        self.exit_btn = Button(self.program_window, text='Sair do Trabalho', font='Arial 14', bg='cyan', command=self.exit_action)
        self.exit_btn.grid(row=7, column=0, columnspan=2, padx=20, pady=10)
            
        # Create label for displaying current system time
        self.clock_lbl = Label(self.program_window, text='', font='Arial 14', bg='#f0f0f0')
        self.clock_lbl.grid(row=8, column=0, columnspan=2, pady=10)
            
        # Update clock label every second
        self.update_clock()
        
        
    def open_window_register(self):
        # Get the username label text in the login window
        username = self.name_lbl.cget('text')
        
        # Pass the username and job options to the other window
        RegisterWindow(username, self.job_options)
        
    
    def open_window_data_list(self):
        DataListWindow()
            

    def enter_action(self):
        # Get current time
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Insert entry time into the database
        self.cursor.execute("INSERT INTO picagem_entrada (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                            (self.get_user_id(), datetime.now().date(), current_time))
        
        # Save to the database
        self.conn.commit()
        
        # Display entry time and message
        self.entry_time_lbl.config(text=f'Entrada: {current_time}\nBom trabalho!')
        
        
    def pause_action(self):
        self.pause_start_time = datetime.now()

        # Exibir mensagem para o funcionário
        current_time = self.pause_start_time.strftime('%H:%M:%S')
        self.entry_time_lbl.config(text=f'Pausa iniciada: {current_time}\nBom almoço!')
        
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
        self.entry_time_lbl.config(text=f'Voltou da Pausa: {current_time}\nDuração da Pausa: {pause_duration_str}')
        
        # Insert pause exit time into the database
        self.cursor.execute("INSERT INTO picagem_saida_pausa (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                            (self.get_user_id(), datetime.now().date(), current_time))
        
        # Save to the database
        self.conn.commit()
        
    
    def exit_action(self):
        # Get current time
        current_time = datetime.now().strftime('%H:%M:%S')
        
        # Insert exit time into the database
        self.cursor.execute("INSERT INTO picagem_saida (id_funcionario, picagem_data, hora_registro) VALUES (?, ?, ?)",
                            (self.get_user_id(), datetime.now().date(), current_time))
        
        # Save to the database
        self.conn.commit()
        
        # Display entry time and message
        self.entry_time_lbl.config(text=f'Saida: {current_time}\nBom trabalho!')
    
    
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
        self.clock_lbl.config(text=f'Hora atual: {current_time}')
        
        # Schedule next update after 1000ms (1 second)
        self.program_window.after(1000, self.update_clock)
    
    
    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()
