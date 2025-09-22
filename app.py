from flask import Flask, request, jsonify, render_template
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import sqlite3
import bcrypt
import re

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute"]
)

class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor()
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

    def close(self):
        self.conn.close()

db = Database('database.db')

def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(not c.isalnum() for c in password)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/users/register', methods=['POST'])
@limiter.limit("100 per minute")
def register_user():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        fullName = data.get('fullName')

        if not email or not password or not fullName:
            return jsonify({'message': 'Missing required fields'}), 400

        if not validate_email(email):
            return jsonify({'message': 'Invalid email'}), 400

        if not validate_password(password):
            return jsonify({'message': 'Password should be at least 8 characters long and contain at least one number and one special character'}), 400

        existing_user = db.get_user_by_email(email)
        if existing_user:
            return jsonify({'message': 'Email already exists'}), 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_id = db.insert_user(email, hashed_password, fullName)

        return jsonify({'message': 'User registered successfully', 'user_id': user_id}), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)