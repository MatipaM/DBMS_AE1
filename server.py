import random
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

def create_user_table():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                profile_picture TEXT,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                email TEXT PRIMARY KEY  NOT NULL,
                password TEXT NOT NULL,
                affiliation TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("User table created successfully")
    except Error as e:
        print(e)

def create_books():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        conn.execute('''CREATE TABLE IF NOT EXISTS Books
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    publisher TEXT NOT NULL,
                    year_purchased TEXT NOT NULL,
                    year_published TEXT NOT NULL,
                    description TEXT NOT NULL,
                    secondary_title TEXT NOT NULL,
                    version TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    available INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    review TEXT,
                    price INTEGER NOT NULL)''')
        # books = [
        #     ('The Great Gatsby', 'F. Scott Fitzgerald', 'Scribner', '2024', '1925', 'A novel set in the Jazz Age', 'None', '1st', 10, 5, 5, 'Excellent', 10),
        #     ('1984', 'George Orwell', 'Secker & Warburg', '2024', '1949', 'A dystopian social science fiction novel', 'None', '1st', 15, 7, 4, 'Thought-provoking', 15),
        #     ('To Kill a Mockingbird', 'Harper Lee', 'J.B. Lippincott & Co.', '2024', '1960', 'A novel about racial injustice', 'None', '1st', 20, 10, 5, 'Timeless classic', 20)
        # ]

        # cursor.executemany('''INSERT INTO Books 
        #                       (title, author, publisher, year_purchased, year_published, description, secondary_title, version, quantity, available, rating, review, price) 
        #                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', books)
        conn.commit()
        cursor.close()
        conn.close()
        print("Book table created successfully")
    except Error as e:
        print(e)

def create_outstanding_bills():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Outstanding_Bills (
                email TEXT PRIMARY KEY  NOT NULL,
                price TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("outstanding bills table created successfully")
    except Error as e:
        print(e)

def create_sales_table():
    # sales_data = [
    #     ("1234", "6894", "1990", 20),
    #     ("2235", "7890", "1987", 19),
    #     ("3345", "8890", "2001", 39),
    #     ("1345", "8890", "2001", 39),
    #     ("3115", "2239", "2002", 15),
    # ]
    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Sales (
                BookID TEXT, 
                SalesID TEXT, 
                Year_Purchased TEXT, 
                Price INTEGER
            )
        ''')
        cursor.execute('ALTER TABLE Sales ADD COLUMN date TEXT')
        conn.commit()

        # for data in sales_data:
        #     cursor.execute('INSERT INTO Sales (BookID, SalesID, Year_Purchased, Price) VALUES (?, ?, ?, ?)', data)
        cursor.close()
        conn.close()
        print("Sales table created successfully")
    except sqlite3.Error as e:
        print(e)

def create_pending_request():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Pending_Request (
                email TEXT NOT NULL,
                date_request TEXT NOT NULL,
                title TEXT NOT NULL,
                interest TEXT NOT NULL,
                affiliation TEXT NOT NULL,
                id TEXT PRIMARY KEY NOT NULL 
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("pending request table created successfully")
    except Error as e:
        print(e)

def create_book_records():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Book_records (
                id TEXT PRIMARY KEY  NOT NULL,
                borrowed_date TEXT NOT NULL,
                returned_date TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Book records table created successfully")
    except Error as e:
        print(e)

@app.route('/outstanding_bills', methods=['POST'])
def save_outstanding_bills():
    create_outstanding_bills()
    print("I am trying to save the pending request's information")
    email = request.json.get('email')
    price = request.json.get('price')

    if not email or not price:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO pending_request (email, price) VALUES (?, ?)', (email, price))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

@app.route('/crazy_books', methods=['POST'])
def save():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No data provided"}), 400

        required = ['title', 'author', 'publisher', 'year_purchased', 'description', 
                           'secondary_title', 'version', 'quantity', 'available', 'rating', 'price']
        
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing required field: {r}"}), 400

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Books (title, author, publisher, year_purchased, year_published, description, 
                                secondary_title, version, quantity, available, rating, 
                                review, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                (data['title'], data['author'], data['publisher'], data['year_purchased'],
                data['year_published'], data['description'], data['secondary_title'], data['version'], 
                int(data['quantity']), int(data['available']), int(data['rating']), 
                data.get('review'), float(data['price']))
            )
            conn.commit()

        return jsonify({"message": "Book submitted successfully"}), 201

    except sqlite3.Error as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500


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

@app.route('/crazy_borrow', methods=['POST'])
def borrow_book():
    try:
        data = request.get_json(force=True)
        print("Received data:", data)
        print("Data type:", type(data))
        print("Email:", data.get('email'))
        print("Date request:", data.get('date_request'))
        print("Books:", data.get('books'))
        
        email = data.get('email')
        date_request = data.get('date_request')
        books = data.get('books')
        

        if not email or not date_request:
            print("Missing data fields:", {"email": email, "date_request": date_request, "books": books})
            return jsonify({'error': 'No data provided'}), 400

        connect = connection()
        cursor = connect.cursor()

        for book in books:
            title = book.get('title')
            interest = book.get('interest')
            affiliation = email.split('@')[1].split('.')[0]
            book_id = str(book.get('id'))  # Convert to string!!!! Thsi caused me headache!!!
            if not all([title, interest, book_id]):
                return jsonify({'error': f'Missing data for book: {book}'}), 400
            cursor.execute('INSERT INTO Pending_Request (email, date_request, title, interest, affiliation, id) VALUES (?, ?, ?, ?, ?, ?)', 
                        (email, date_request, title, interest, affiliation, book_id))
            connect.commit()
            cursor.close()
            connect.close()

            return jsonify({'message': 'Data saved'}), 201
    except sqlite3.Error as e:
        print("SQLite error:", e)
        if connect:
            connect.rollback()
        return jsonify({'error': 'Database error'}), 500
    except Exception as e:
        print("Other error:", e)
        if connect:
            connect.rollback()
        return jsonify({'error': 'Error processing request'}), 500

@app.route('/crazy_return', methods=['POST'])
def return_book():
    create_book_records()
    print("I am trying to save the book records's information")
    borrowed_date = request.json.get('borrowed_date')
    returned_date = request.json.get('returned_date')
    email = request.json.get('email')
    id = request.json.get('id')

    if not email or not borrowed_date or not returned_date or not id: 
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO book_records (email, borrowed_date, returned_date, id) VALUES (?, ?, ?, ?, ?, ?)', (email, borrowed_date, returned_date, id))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500
    pass

@app.route('/crazy_sale', methods=['POST'])
def save_sale():
    #sales_table()
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
        cursor.execute('INSERT INTO Sales (BookID, SalesID, Year_Purchased, Price) VALUES (?, ?, ?, ?)', (book_id, sales_id, year_purchased, price))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500


create_book_records()
create_books()
create_outstanding_bills()
create_pending_request()
create_sales_table()
create_user_table()

if __name__ == '__main__':
    create_books()  # Call create_books() only if running this script directly
    #sales_table()   # Call sales_table() only if running this script directly
    app.run(port=5000)
