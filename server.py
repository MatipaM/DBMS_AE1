from flask import Flask, request, jsonify
#import mysql.connector
#from mysql.conncetor import Error
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

#def connection():
#    return mysql.connector.connect(
#                host='localhost',
#                user='username',
#                password='password',
#                database='database'
#            )


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
    if not title or not author:
        return jsonify({'error': 'No data provided'}), 400
<<<<<<< Updated upstream
=======

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
>>>>>>> Stashed changes
    
    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Books (title, author) VALUES (?, ?)', (title, author))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except:
        return jsonify({'error': 'Error saving data'}), 500
<<<<<<< Updated upstream
=======

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

>>>>>>> Stashed changes
    
if __name__ == '__main__':
    app.run(port=5000)