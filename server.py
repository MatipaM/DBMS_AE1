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
    if not title or not author:
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

# USER TABLES
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

def create_table(table_name):
    print(f"attempting to create {table_name}")
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS {table_name} (
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
        print(f"{table_name} created successfully")
    except Error as e:
        print(e)

@app.route('/crazy_librarian', methods=['POST'])
def save_librarian():
    create_table("Librarian")
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
        cursor.execute('INSERT INTO librarian (first_name, last_name, profile_picture, address, phone, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, profile_picture, address, phone, email, password))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500


@app.route('/crazy_administrator', methods=['POST'])
def save_administrator():
    create_table("Administrator")
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
        cursor.execute('INSERT INTO Administrator (first_name, last_name, profile_picture, address, phone, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, profile_picture, address, phone, email, password))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500


@app.route('/crazy_student', methods=['POST'])
def save_student():
    create_table("Student")
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
        cursor.execute('INSERT INTO Student (first_name, last_name, profile_picture, address, phone, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, profile_picture, address, phone, email, password))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500


@app.route('/crazy_staff', methods=['POST'])
def save_staff():
    create_table("Staff")
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
        cursor.execute('INSERT INTO Staff (first_name, last_name, profile_picture, address, phone, email, password) VALUES (?, ?, ?, ?, ?, ?, ?)', (first_name, last_name, profile_picture, address, phone, email, password))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

# Create Sales Table
def sales_table():
    sales_data = [
        ("1234", "6894", "1990", 20),
        ("2235", "7890", "1987", 19),
        ("3345", "8890", "2001", 39),
        ("1345", "8890", "2001", 39),
        ("3115", "2239", "2002", 15),
    ]
    try:
        connect = connection()
        cursor = connect.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sales (
                BookID TEXT, 
                SalesID TEXT, 
                Year_Purchased TEXT, 
                Price INTEGER
            )
        ''')
        connect.commit()

        for data in sales_data:
            cursor.execute('INSERT INTO Sales (BookID, SalesID, Year_Purchased, Price) VALUES (?, ?, ?, ?)', data)

        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except sqlite3.Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

def transaction_table():
    try:
        connect = connection()
        cursor = connect.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Transaction (
                SalesID TEXT, 
                Date TEXT
            )
        ''')
        connect.commit()

        data = ("1234", "2021-09-01")

        cursor.execute('INSERT INTO Transaction (SalesID, Date) VALUES (?, ?)', data)
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except sqlite3.Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

@app.route('/create_table', methods=['POST'])
def create_table():
    return transaction_table()

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
        #There is a bug in not deleting the row from Books
        cursor.execute('DELETE FROM Books WHERE Title = ?', (title,))
        connect.commit()
        cursor.close()
        connect.close()

        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500
    
# Book Availability Function

if __name__ == '__main__':
    app.run(port=5000)    

sales_table()