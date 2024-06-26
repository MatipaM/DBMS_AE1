from flask import Flask, make_response, request, jsonify
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
    version = request.json.get('version')
    secondary_title = request.json.get('secondary_title')  
    year_purchased = request.json.get('year_purchased')
    quantity = request.json.get('quantity')

    print("code part 2 running")
 
    # if not title or not author or not publisher or not description or not version or not secondary_title or not year_purchased:
    if not title or not author or not publisher or not description or not version or not secondary_title or not year_purchased or not quantity:
        print(f"no data provided: title:{title} {author} {publisher} {description} {version} {secondary_title} {year_purchased} {quantity}")
        return jsonify({'error': 'No data provided'}), 400

    try:
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
        return make_response('Data saved', 201)
    except sqlite3.Error as e:
        print(e)
        return make_response('Error saving data', 500)
    
@app.route('/crazy_sale', methods=['POST'])
def save_sale():
    sales_table()
    print("I am trying to save the sales information")
    book_id = request.json.get('book_id')
    sales_id = request.json.get('sales_id')
    year_purchased = request.json.get('year_purchased')
    price = request.json.get('price')  

    if not book_id or not sales_id or not year_purchased or not price:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO USER (book_id, sales_id, year_purchased, price) VALUES (?, ?, ?, ?)', (book_id, sales_id, year_purchased, price))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

create_books()
sales_table()


if __name__ == '__main__':
    app.run(port=5000)   


