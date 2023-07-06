import hashlib
import sqlite3
from getpass import getpass

from flask import Flask, request

DB_NAME = 'users.db'
TABLE_NAME = 'users'
SCHEMA = '''CREATE TABLE IF NOT EXISTS {} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
)'''.format(TABLE_NAME)

app = Flask(__name__)
app.secret_key = 'secret_key'

def generate_password_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()

def store_user(username, password):
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO {} (username, password_hash) VALUES (?, ?)'.format(TABLE_NAME), (username, password_hash))
    conn.commit()
    conn.close()

def validate_user(username, password):
    password_hash = generate_password_hash(password)
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} WHERE username=? AND password_hash=?'.format(TABLE_NAME), (username, password_hash))
    result = cursor.fetchone()
    conn.close()
    return result is not None

@app.route('/login', methods=['GET'])
def login():
    username = request.form['username']
    password = request.form['password']
    if validate_user(username, password):
        return 'Login exitoso'
    else:
        return 'Login fallado'

if __name__ == '__main__':
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(SCHEMA)
    conn.close()

    store_user('FERNANDEZ', 'NF')
    store_user('NUNEZ', 'JN')
    store_user('TOLOZA', 'IT')

app.run(port=9500)
