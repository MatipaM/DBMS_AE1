from flask import Flask, request, jsonify
import sqlite3
from sqlite3 import Error

app = Flask(__name__)


def connection():
    conn = None
    try:
        conn = sqlite3.connect('database.db')
    except Error as e:
        print(e)
    return conn

@app.route('/crazy_books', methods=['POST'])
def save():
    title = request.json.get('title')
    author = request.json.get('author')
    publisher = request.json.get('publisher')
    description = request.json.get('description')  
    secondary_title = request.json.get('secondary_title')
    version = request.json.get('publisher')
    year_purchased= request.json.get('year_purchased')  

    if not title or not author or not publisher or not description or not secondary_title or not version or not year_purchased:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Books (title, secondary_title, author, publisher, description, version, year_purchased) VALUES (?, ?, ?, ?, ?, ?, ?)', (title, author, publisher, description, secondary_title, version, year_purchased))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

# Borrow Book Function

@app.route('/crazy_borrow', methods=['POST'])
def borrow_book():
    user_id = request.json.get('user_id')
    book_title = request.json.get('book_title')
    date_borrowed = request.json.get('date_borrowed')  

    if not user_id or not book_title or not date_borrowed:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Borrow (user_id, Title, Borrowed_Date) VALUES (?, ?, ?)', (user_id, book_title, date_borrowed))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

    

# USER TABLE

@app.route('/crazy_user', methods=['POST'])
def save_user():
    create_user_table()
    print("I am trying to save the user's information")
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    profile_picture = request.json.get('profile_picture')
    address = request.json.get('address')  
    phone = request.json.get('phone')
    email = request.json.get('email')
    password= request.json.get('password')  

    if not first_name or not last_name or not profile_picture or not address or not phone or not email or not password:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO USER (first_name, last_name, profile_picture, address, phone, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, profile_picture, address, phone, email, password))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

def create_user_table():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                profile_picture TEXT,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("User table created successfully")
    except Error as e:
        print(e)
    
if __name__ == '__main__':
    app.run(port=5000)
    
