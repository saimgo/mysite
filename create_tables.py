# create_tables.py
import sqlite3

# Function to create tables in the SQLite database
def create_tables():
    conn = sqlite3.connect('site.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
                        id INTEGER PRIMARY KEY,
                        title TEXT NOT NULL,
                        content TEXT NOT NULL,
                        author TEXT NOT NULL,
                        category TEXT NOT NULL
                        
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL,
                    message TEXT NOT NULL
                )''')


    cursor.execute('''INSERT INTO users (username, password) VALUES (?, ?)''', ('saim001', 'saim24@stella'))

    conn.commit()
    conn.close()

# Call the function to create tables
if __name__ == '__main__':
    create_tables()
