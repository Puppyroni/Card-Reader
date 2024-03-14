import sqlite3

# connect to a database
conn = sqlite3.connect('temp.db')

# Create a cursor
cursor = conn.cursor()

# Command SQL for creating a table
# ID int PK
# USER text not null unique
# PASSWORD text not null
create_table = '''
    CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY,
        user TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
'''

# Execute the SQL command with cursor
cursor.execute(create_table)

# Save with the commit
conn.commit()

# Close the connection
conn.close()

# Confirmation that the code has been successful at saving the data
print('Saved Successfully!')