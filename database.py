import sqlite3

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                fullName TEXT NOT NULL
            );
        ''')
        self.conn.commit()

    def get_user_by_email(self, email):
        self.cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        return self.cursor.fetchone()

    def insert_user(self, email, password, fullName):
        self.cursor.execute('INSERT INTO users (email, password, fullName) VALUES (?, ?, ?)', (email, password, fullName))
        self.conn.commit()
        return self.cursor.lastrowid