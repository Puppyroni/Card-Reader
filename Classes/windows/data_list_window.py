from customtkinter import *
from customtkinter import CTk
from CTkListbox import *
import tkinter.simpledialog as spldialog
from tkinter import messagebox
import sqlite3

class DataListWindow:
    def __init__(self, username, user_role):
        # Create the main window
        self.data_list_window = CTkToplevel()
        self.data_list_window.title('Lista de Dados')
        self.data_list_window.resizable(False, False)
        
        # Load and set custom icon
        try:
            icon_path = 'Assets/icons/icon.ico'
            self.data_list_window.iconbitmap(icon_path)
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print('Error setting icon:', e)
        
        self.data_list_window.configure(bg='#f0f0f0')
        
        # Save user role for future reference
        self.user_role = user_role
        
        # Connect to a database
        self.conn = sqlite3.connect('User_Data.db')
        self.cursor = self.conn.cursor()
        
        print(username)
        
        # Configure a button for the list of users
        self.users_btn = CTkButton(self.data_list_window, text='Utilizador', command=lambda: self.populate_listbox("users"))
        self.users_btn.grid(row=0, column=0, columnspan=2, padx=20, pady=20)
        
        # Configure a button for worker's schedule
        self.schedule_btn = CTkButton(self.data_list_window, text='Horários', command=lambda: self.populate_listbox("schedules"))
        self.schedule_btn.grid(row=0, column=2, columnspan=2, padx=20, pady=20)
        
        # Configure a button for worker's schedule
        self.clocked_in_btn = CTkButton(self.data_list_window, text='Entradas', command=lambda: self.populate_listbox("clocked in"))
        self.clocked_in_btn.grid(row=0, column=4, columnspan=2, padx=20, pady=20)
        
        # Configure a button for the list of department
        self.department_btn = CTkButton(self.data_list_window, text='Cargo', command=lambda: self.populate_listbox("department"))
        self.department_btn.grid(row=0, column=6, columnspan=2, padx=20, pady=20)
        
        # Create a Listbox widget
        self.data_listbox = CTkListbox(self.data_list_window, width=500, height=300)
        self.data_listbox.grid(row=1, column=0, columnspan=6, padx=20, pady=20)
        
        # Create label for user filter
        self.username_lbl = CTkLabel(self.data_list_window, text='Horário Filtro por Utilizador:', fg_color="transparent")
        self.username_lbl.grid(row=2, column=0, pady=20, sticky='E')
        
        # Create a variable to store the selected user
        self.selected_user = StringVar(self.data_list_window)
        self.selected_user.set('All')  # Initialize with empty value
        
        # Check the query for a SuperUser, Admin, or Chief
        self.cursor.execute("""
            SELECT funcionarios.*, cargo.cargo_nome FROM funcionarios
            INNER JOIN cargo ON funcionarios.cargo_id = cargo.id
            WHERE funcionarios.nome=? 
            AND (cargo.cargo_nome='SuperUser' OR cargo.cargo_nome='Admin' OR cargo.cargo_nome='Gerente')
        """, (username,))
        result_superuser_admin= self.cursor.fetchone()

        # Check if the entered username is a SuperUser, Admin, or Chief
        if result_superuser_admin:
            # Configure a button of Remove User
            self.rmv_user_sp_admin_btn = CTkButton(self.data_list_window, text = 'Remover Utilizador', command = self.bind_click)
            self.rmv_user_sp_admin_btn.grid(row = 2, column = 2, columnspan = 2, padx = 20, pady = 10, sticky='E')
            
            # Configure a button of Add Department
            self.Schedule_btn = CTkButton(self.data_list_window, text = 'Adicionar Cargo', command = self.add_department)
            self.Schedule_btn.grid(row = 2, column = 4, columnspan = 2, padx = 20, pady = 10, sticky='E')
        
        # Fetch data from the database and populate the listbox
        self.populate_listbox('users')

    def add_department(self):
        # Create Input prompt
        department_name = spldialog.askstring('Novo Cargo', 'Escreva o nome do novo cargo:')
         
        # Insert the output from the prompt into the database
        self.cursor.execute('INSERT INTO cargo (cargo_nome) VALUES (?)',(department_name,))
        
        # Save to the Database
        self.conn.commit()
        
        
    def bind_click(self):
        # Define a method to bind the button to remove_user
        def bind_remove_user(event=None):
            self.remove_user()
            self.rmv_user_sp_admin_btn.unbind("<ButtonRelease-1>")
        
        # Bind the button to the method defined above using single-click event
        self.rmv_user_sp_admin_btn.bind("<ButtonRelease-1>", bind_remove_user)

        

    def remove_user(self):
        # Get the index of the selected item
        selected_index = self.data_listbox.curselection()
        
        # Check if any item is selected in the listbox and the selected index is not 0
        if selected_index or selected_index == 0:
            # If an item is selected and the index is not 0, proceed with removal
            selected_item = self.data_listbox.get(selected_index)
            user_id, username = selected_item.split(' || ')[0], selected_item.split(' || ')[1]
            
            # Prompt user for confirmation
            confirmation = messagebox.askyesno("Confirmação", f"Tem a certeza de que pretende remover o utilizador {username}?")
            if confirmation:
                # Query for the user id
                self.cursor.execute("SELECT id FROM funcionarios WHERE id=?", (user_id,))
                result_user = self.cursor.fetchone()
                    
                # If a user id exists, delete it
                if result_user:
                    # Delete user from the database
                    self.cursor.execute("DELETE FROM funcionarios WHERE id=?", (user_id,))
                        
                    # Save to the database
                    self.conn.commit()
                    
                    # Remove the item from the listbox
                    self.data_listbox.delete(selected_index)
                    
        else:
            # If no item is selected or the selected index is 0, display a message or handle it appropriately
            messagebox.showinfo("Sem seleção", "Please select a correct user to remove.")


    def populate_listbox(self, data_type):
        # Clear the listbox before populating again
        self.data_listbox.delete(0, 'end')

        # Fetch usernames from the database
        self.cursor.execute("SELECT nome FROM funcionarios")
        user_records = self.cursor.fetchall()
        
        # Extracting usernames
        user_options = [record[0] for record in user_records]

        # Update the dropdown list with fetched usernames and additional options
        options = ['All'] + user_options
        
        # Recreate the option menu with updated options
        self.user_option = CTkOptionMenu(self.data_list_window, variable=self.selected_user, values=options)
        self.user_option.grid(row=2, column=1, pady=20, sticky='E')
        
        # Filter data based on the selected user
        if self.selected_user.get() == 'All':
            where_condition = ""  # Show all users
            
            # Adjust where_condition based on user role
            if self.user_role == 'SuperUser':
                # SuperUser sees all users, so no filtering required
                where_condition = ""
            elif self.user_role == 'Admin':
                # Admin sees all users except SuperUsers
                where_condition = "WHERE c.cargo_nome != 'SuperUser'"
            elif self.user_role == 'Gerente':
                # Manager sees all users except SuperUsers and Admins
                where_condition = "WHERE c.cargo_nome NOT IN ('SuperUser', 'Admin')"
            else:
                # Other roles see all users (no filtering)
                where_condition = ""
        elif self.selected_user.get() or data_type == "users":
            where_condition = f"WHERE f.nome = '{self.selected_user.get()}'"  # Filter by selected user
            
            # Adjust where_condition based on user role
            if self.user_role == 'SuperUser':
                # SuperUser sees all users, so no filtering required
                where_condition = where_condition + ""
            elif self.user_role == 'Admin':
                # Admin sees all users except SuperUsers
                where_condition = where_condition + "AND c.cargo_nome != 'SuperUser'"
            elif self.user_role == 'Gerente':
                # Manager sees all users except SuperUsers and Admins
                where_condition = where_condition + "AND c.cargo_nome NOT IN ('SuperUser', 'Admin')"
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
                SELECT f.id, f.nome, f.idade, f.morada, c.cargo_nome FROM funcionarios f 
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
            self.data_listbox.insert('end', display_text)


    def __del__(self):
        # Close the database connection when the object is destroyed
        self.conn.close()
