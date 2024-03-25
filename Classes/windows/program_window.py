from tkinter import *
from datetime import datetime, timedelta
from tkinter import messagebox
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
        self.program_window.geometry("1000x600")  # Definir o tamanho da janela
         
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
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND (cargo='SuperUser' or cargo='Admin' or cargo='Chefe')", (username,))
        result_job = self.cursor.fetchone()
        
        # Check if the entered username is a SuperUser
        if result_job:
            # Configure a button of register
            self.register_btn = Button(self.program_window, text = 'Register', font = 'Arial 14', bg = 'cyan', command = self.open_window_register)
            self.register_btn.grid(row = 17, column = 2, columnspan = 2, padx = 20, pady = 10)
            
            # Configure a button of worker's schedule TEMP: for now uses register Button
            self.Schedule_btn = Button(self.program_window, text = 'Schedules', font = 'Arial 14', bg = 'cyan', command = self.open_window_data_list)
            self.Schedule_btn.grid(row = 18, column = 2, columnspan = 2, padx = 20, pady = 10)
            
        # Check the quary for a SuperUser
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='SuperUser'", (username,))
        result_superuser = self.cursor.fetchone()
        
            
        # Check the quary for a Admin 
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='Admin'", (username,))
        result_admin = self.cursor.fetchone()
        
        # Check if the entered username is a a Admin
       
            
            
        # Check the quary for a Chefe 
        self.cursor.execute("SELECT * FROM funcionarios WHERE nome=? AND cargo='Chefe'", (username,))
        result_chief = self.cursor.fetchone()
        
        # Check if the entered username is a Chefe
        if result_chief:
            # Allow ability to Create workers
            self.temp_lbl = Label(self.program_window, text = '', font = 'Arial 14 bold', bg = '#f0f0f0')
            self.temp_lbl.grid(row = 9, column = 5, pady = 20, sticky = 'E')
            
        self.enter_btn = Button(self.program_window, text='Entrar', font='Arial 14', bg='#4CAF50', fg='white', command=self.enter_action)
        self.enter_btn.grid(row=6, column=0, padx=20, pady=10)

        self.pause_btn = Button(self.program_window, text='Pausa', font='Arial 14', bg='#FFC107', fg='white', command=self.pause_action)
        self.pause_btn.grid(row=6, column=1, padx=20, pady=10)

        self.resume_btn = Button(self.program_window, text='Voltar da Pausa', font='Arial 14', bg='#FF9800', fg='white', command=self.resume_action)
        self.resume_btn.grid(row=6, column=2, padx=20, pady=10)

        self.exit_btn = Button(self.program_window, text='Sair do Trabalho', font='Arial 14', bg='#F44336', fg='white', command=self.exit_action)
        self.exit_btn.grid(row=6, column=3, padx=20, pady=10)

        # Configure labels with improved design
        self.entry_time_lbl = Label(self.program_window, text='', font='Arial 14', bg='#f0f0f0', fg='#333')
        self.entry_time_lbl.grid(row=7, column=0, columnspan=4, padx=20, pady=10)

        self.clock_lbl = Label(self.program_window, text='', font='Arial 14', bg='#f0f0f0', fg='#333')
        self.clock_lbl.grid(row=8, column=0, columnspan=4, pady=10)
            
        # Update clock label every second
        self.update_clock()
        
        
    def open_window_register(self):
        # Get the username label text in the login window
        username = self.name_lbl.cget('text')
        
         # Pass the username to the other window
        RegisterWindow(username)
        
    
    def open_window_data_list(self):
        # Consulta SQL para selecionar os funcionários que estão trabalhando atualmente
        current_time = datetime.now().strftime('%H:%M:%S')
        query = """
        SELECT funcionarios.nome 
        FROM picagem_entrada 
        INNER JOIN funcionarios ON picagem_entrada.id_funcionario = funcionarios.id 
        WHERE ? BETWEEN picagem_entrada.hora_registro 
        AND (SELECT picagem_saida.hora_registro 
            FROM picagem_saida 
            WHERE picagem_entrada.id_funcionario = picagem_saida.id_funcionario 
            ORDER BY picagem_saida.hora_registro DESC 
            LIMIT 1)
        """
        self.cursor.execute(query, (current_time,))
        working_employees = self.cursor.fetchall()

        # Exibir uma mensagem com os funcionários que estão trabalhando atualmente
        if working_employees:
            employee_names = "\n".join([employee[0] for employee in working_employees])
            messagebox.showinfo("Funcionários Trabalhando Agora", f"Os seguintes funcionários estão trabalhando agora:\n{employee_names}")
        else:
            messagebox.showinfo("Funcionários Trabalhando Agora", "Não há funcionários trabalhando neste momento.")


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