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
    print("save book function called")
    title = request.json.get('title')
    author = request.json.get('author')
    publisher = request.json.get('publisher')
    description = request.json.get('description')
    version = request.json.get('version')
    secondary_title = request.json.get('secondary_title')  
    year_purchased = request.json.get('year_purchased')
    quantity = request.json.get('quantity')

    print("code part 2 running")
 
    # if not title or not author or not publisher or not description or not version or not secondary_title or not year_purchased:
    if not title or not author or not publisher or not description or not version or not secondary_title or not year_purchased or not quantity:
        print(f"no data provided: title:{title} {author} {publisher} {description} {version} {secondary_title} {year_purchased} {quantity}")
        return jsonify({'error': 'No data provided'}), 400
    else:
        print("all information input")

    try:
        print("attempting to save book")
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Books (title, secondary_title, author, publisher, description, version, year_purchased, quantity) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (title, secondary_title, author, publisher, description, version, year_purchased, quantity))
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
                affiliation TEXT NOT NULL
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

# USER TABLES
@app.route('/crazy_user', methods=['POST'])
def save_user():
    create_user_table()
    print("I am trying to save the user's information")
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    profile_picture = request.json.get('profile_picture')
    address = request.json.get('address')  
    affiliation = request.json.get('affiliation')  
    phone = request.json.get('phone')
    email = request.json.get('email')
    password= request.json.get('password')  

    if not first_name or not last_name or not profile_picture or not address or not phone or not email or not password or not affiliation:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO USER (first_name, last_name, profile_picture, address, affiliation, phone, email, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, profile_picture, address, affiliation, phone, email, password))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500
    
def create_books():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publisher TEXT,
                year_purchased TEXT NOT NULL,
                description TEXT NOT NULL,
                secondary_title TEXT NOT NULL,
                version TEXT NOT NULL,
                quantity INTEGER NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Book table created successfully")
    except Error as e:
        print(e)

# Borrow Book Function

@app.route('/crazy_borrow', methods=['POST'])
def borrow_book():
    email = request.json.get('email')
    title = request.json.get('title')
    affiliation = request.json.get('affiliation')
    interest = request.json.get('interest')
    request_date = request.json.get('request_date')
    
    if not email or not title or not affiliation or not interest or not request_date:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Pending_Request (Email, Title, Affiliation, Interest, Request_Date) VALUES (?, ?, ?, ?, ?)', (email, title, affiliation, interest, request_date))
        connect.commit()
        cursor.close()
        connect.close()

        #session['email'] = email

        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

# Book Return Function
@app.route('/crazy_return', methods=['POST'])
def return_book():
    email = request.json.get('email')
    title = request.json.get('title')
    returned_date = request.json.get('returned_date')
    rating = request.json.get('rating')
    review = request.json.get('review')

    if not email or not title or not returned_date:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('UPDATE Book_Records SET Returned_Date = ?, Rating = ?, Review = ? WHERE Email = ? AND Title = ?', (returned_date, rating, review, email, title))
        cursor.execute('DELETE FROM Books WHERE Title = ?', (title,))
        connect.commit()
        cursor.close()
        connect.close()

        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500
    
# Book Availability Function

create_books()


if __name__ == '__main__':
    app.run(port=5000)   

