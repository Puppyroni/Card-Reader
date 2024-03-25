import sqlite3

try:
    # Connect to a database
    conn = sqlite3.connect('User_Data.db')

    # Create a cursor
    cursor = conn.cursor()

    # Command SQL for creating tables
    create_tables = '''
        
    '''

    # Execute the SQL command with cursor
    cursor.executescript(create_tables)

    # Save with the commit
    conn.commit()

    # Close the connection
    conn.close()

    # Confirmation that the code has been successful at saving the data
    print('Saved Successfully!')

except sqlite3.Error as e:
    print('SQLite error:', e)
