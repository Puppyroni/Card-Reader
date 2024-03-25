from tkinter import *
import sqlite3

class DataListWindow:
    def __init__(self, username):
        # Create the main window
        self.data_list_window = Toplevel()
        self.data_list_window.title('Data List')
        self.data_list_window.iconbitmap('Assets/icons/icon.ico')
        self.data_list_window.configure(bg='#f0f0f0')
        
        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()
        
        # Configure a button for the list of users
        self.users_btn = Button(self.data_list_window, text='Users', font='Arial 14', bg='cyan', command=lambda: self.populate_listbox("users"))
        self.users_btn.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        
        # Configure a button for worker's schedule
        self.schedule_btn = Button(self.data_list_window, text='Schedules', font='Arial 14', bg='cyan', command=lambda: self.populate_listbox("schedules"))
        self.schedule_btn.grid(row=0, column=1, columnspan=2, padx=20, pady=20)
        
        # Configure a button for worker's schedule
        self.clocked_in_btn = Button(self.data_list_window, text='Clocked In', font='Arial 14', bg='cyan', command=lambda: self.populate_listbox("clocked in"))
        self.clocked_in_btn.grid(row=0, column=2, columnspan=2, padx=20, pady=20)
        
        # Configure a button for the list of department
        self.department_btn = Button(self.data_list_window, text='Department', font='Arial 14', bg='cyan', command=lambda: self.populate_listbox("department"))
        self.department_btn.grid(row=0, column=4, columnspan=2, padx=20, pady=20)
        
        # Create a Listbox widget
        self.data_listbox = Listbox(self.data_list_window, width=50, height=20)
        self.data_listbox.grid(row=1, column=0, columnspan=6, padx=20, pady=20)
        
        # Create label for user filter
        self.username_lbl = Label(self.data_list_window, text='Schedule Filter by User:', font='Arial 14 bold', bg='#f0f0f0')
        self.username_lbl.grid(row=2, column=0, pady=20, sticky='E')
        
        # Create a variable to store the selected user
        self.selected_user = StringVar(self.data_list_window)
        self.selected_user.set('All')  # Set Default to All
        
        # Create a dropdown list widget
        self.user_option = OptionMenu(self.data_list_window, self.selected_user, '')
        self.user_option.config(font='Arial 14 bold', bg='#f0f0f0', width=15)
        self.user_option.grid(row=2, column=1, pady=20, sticky='E')
        
        # Check the query for a SuperUser, Admin, or Chief
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? 
            AND (cargo.cargo_nome='SuperUser' OR cargo.cargo_nome='Admin')
        """, (username,))
        result_superuser_admin= self.cursor.fetchone()

        # Check if the entered username is a SuperUser, Admin, or Chief
        if result_superuser_admin:
            # Configure a button of 
            self.register_btn = Button(self.data_list_window, text = 'Remove User', font = 'Arial 14', bg = 'cyan', command = self.populate_listbox)
            self.register_btn.grid(row = 2, column = 2, columnspan = 2, padx = 20, pady = 10, sticky='E')
            
            # Configure a button of 
            self.Schedule_btn = Button(self.data_list_window, text = 'Add Department', font = 'Arial 14', bg = 'cyan', command = self.populate_listbox)
            self.Schedule_btn.grid(row = 2, column = 4, columnspan = 2, padx = 20, pady = 10, sticky='E')
        
        # Check the query for a Chief
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? 
            AND (cargo.cargo_nome='Chefe')
        """, (username,))
        result_maneger= self.cursor.fetchone()

        # Check if the entered username is a chief
        # Block them for removing SuperUser
        # not working
        if result_maneger:
            # Configure a button of 
            self.register_btn = Button(self.data_list_window, text = 'Remove User', font = 'Arial 14', bg = 'cyan', command = self.populate_listbox)
            self.register_btn.grid(row = 2, column = 2, columnspan = 2, padx = 20, pady = 10, sticky='E')
        
        # Fetch data from the database and populate the listbox
        self.populate_listbox("users")


    def populate_listbox(self, data_type):
        # Clear the listbox before populating again
        self.data_listbox.delete(0, 'end')

        # Fetch usernames from the database
        self.cursor.execute("SELECT nome FROM funcionarios")
        user_records = self.cursor.fetchall()
        
        # Extracting usernames
        user_options = [record[0] for record in user_records]

        # Update the dropdown list with fetched usernames
        self.user_option['menu'].delete(0, 'end')

        # Add an empty option to list all users
        self.user_option['menu'].add_command(label='All', command=lambda usr='All': self.selected_user.set(usr))

        # Add the fetched usernames to the dropdown list
        for user in user_options:
            self.user_option['menu'].add_command(label=user, command=lambda usr=user: self.selected_user.set(usr))

        # Filter data based on the selected user
        if self.selected_user.get() == 'All':
            where_condition = ""  # Show all users
        elif self.selected_user.get() or data_type == "users":
            where_condition = f"WHERE f.nome = '{self.selected_user.get()}'"  # Filter by selected user
        else:
            where_condition = ""

        # Construct the SQL query based on data type
        if data_type == "schedules":
            # Create a List of the schedules from 4 Tables(picagem_entrada, picagem_entrada_pausa, picagem_saida_pausa, picagem_saida) in databese 
            query = f"""
                SELECT f.nome, pe.picagem_data, pe.hora_registro, 'Entrada' AS source
                FROM funcionarios f JOIN picagem_entrada pe ON f.id = pe.id_funcionario
                {where_condition}
                UNION
                SELECT f.nome, pep.picagem_data, pep.hora_registro, 'Entrada de Pausa' AS source
                FROM funcionarios f JOIN picagem_entrada_pausa pep ON f.id = pep.id_funcionario
                {where_condition}
                UNION
                SELECT f.nome, psp.picagem_data, psp.hora_registro, 'Saida de Pausa' AS source
                FROM funcionarios f JOIN picagem_saida_pausa psp ON f.id = psp.id_funcionario
                {where_condition}
                UNION
                SELECT f.nome, ps.picagem_data, ps.hora_registro, 'Saida' AS source
                FROM funcionarios f JOIN picagem_saida ps ON f.id = ps.id_funcionario
                {where_condition}"""
        elif data_type == "users":
            # Create a List of info users from 2 Tables(funcionarios, cargo) in databese 
            query = f"""
                SELECT f.nome, f.idade, f.morada, c.cargo_nome FROM funcionarios f 
                INNER JOIN cargo c ON f.cargo_id = c.id 
                {where_condition}"""
        elif data_type == "clocked in":
            # Create a List of who clocked in from 2 Tables(funcionarios, cargo) in databese 
            query = f"""
                SELECT f.nome, f.idade, f.morada, c.cargo_nome FROM funcionarios f 
                INNER JOIN cargo c ON f.cargo_id = c.id
                WHERE f.id IN (
                    SELECT id_funcionario FROM picagem_entrada 
                    WHERE picagem_data = DATE('now')
                ) 
                AND f.id NOT IN (
                    SELECT id_funcionario FROM picagem_saida 
                    WHERE picagem_data = DATE('now')
                )
                {where_condition}"""
        elif data_type == "department":
            # Create a List of Departments
            query = "SELECT cargo_nome FROM cargo"
            where_condition = ""  # Departments are not filtered
        
        # Execute the query
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        
        # Insert data into the listbox
        for row in data:
            # Concatenate the values of desired columns into a single string
            display_text = " || ".join(str(cell) for cell in row)
            self.data_listbox.insert(END, display_text)
