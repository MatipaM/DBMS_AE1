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

def create_admin_audit():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Admin_Auditing (
                email text PRIMARY KEY,
                approved_date TEXT,
                approved_admin_email TEXT,
                approved_status TEXT
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Admin auditing table created successfully")
    except Error as e:
        print(e)


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
                returned_date TEXT,
                email TEXT NOT NULL
            )
        ''')
        conn.commit()
        cursor.close()
        conn.close()
        print("Book records table created successfully")
    except Error as e:
        print(e)

def addbookandsales():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM Books")
    existing_ids = set(row[0] for row in cursor.fetchall())

    books_data = [
        (1, "The Great Gatsby", "F. Scott Fitzgerald", "Scribner", "2004", "1925", "A classic novel of the Roaring Twenties", "N/A", "1st", 10, 10, 5, "Great book", 15),
        (2, "To Kill a Mockingbird", "Harper Lee", "J.B. Lippincott & Co.", "2010", "1960", "A novel about racial injustice in the Deep South", "N/A", "1st", 8, 8, 5, "Must read", 10),
        (3, "1984", "George Orwell", "Secker & Warburg", "1990", "1949", "A dystopian social science fiction novel", "N/A", "1st", 12, 12, 5, "Very relevant", 20),
        (4, "Pride and Prejudice", "Jane Austen", "T. Egerton", "2000", "1813", "A romantic novel of manners", "N/A", "1st", 15, 15, 5, "Classic novel", 12),
        (5, "The Catcher in the Rye", "J.D. Salinger", "Little, Brown and Company", "1991", "1951", "A story about adolescent alienation", "N/A", "1st", 20, 20, 5, "Timeless read", 18)
    ]

    books_data = [book for book in books_data if book[0] not in existing_ids]

    cursor.executemany("""
        INSERT INTO Books (id, title, author, publisher, year_purchased, year_published, description, secondary_title, version, quantity, available, rating, review, price) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, books_data)

    sales_data = [
        ("1", "S001", "2023", 15, "2023-06-01"),
        ("2", "S002", "2023", 10, "2023-06-02"),
        ("3", "S003", "2023", 20, "2023-06-03"),
        ("1", "S004", "2023", 15, "2023-06-04"),
        ("2", "S005", "2023", 10, "2023-06-05")
    ]

    cursor.executemany("""
        INSERT INTO Sales (BookID, SalesID, Year_Purchased, Price, date) 
        VALUES (?, ?, ?, ?, ?)
    """, sales_data)

    conn.commit()
    conn.close()

#addbookandsales()


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
                           'secondary_title', 'version', 'available', 'rating', 'price']
        
        for r in required:
            if r not in data:
                return jsonify({"error": f"Missing required field: {r}"}), 400

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO Books (title, author, publisher, year_purchased, year_published, description, 
                                secondary_title, version, available, rating, 
                                review, price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', 
                (data['title'], data['author'], data['publisher'], data['year_purchased'],
                data['year_published'], data['description'], data['secondary_title'], data['version'], 
                int(data['available']), int(data['rating']), 
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
    data = request.get_json(force=True)
    print(f"Processed data: {data}")

    email = data.get('email')
    title = data.get('title')
    returned_date = data.get('returned_date')
    rating = data.get('rating')
    review = data.get('review')

    if not email or not title or not returned_date or not rating or not review:
        return jsonify({'error': 'Missing required data'}), 400

    try:
        conn = connection()
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM Books WHERE title = ?', (title,))
        book_id_result = cursor.fetchone()
        if not book_id_result:
            return jsonify({'error': 'Book not found'}), 404
        book_id = book_id_result[0]

        cursor.execute('''
            UPDATE Book_records
            SET returned_date = ?
            WHERE email = ? AND id = ? AND returned_date IS NULL
        ''', (returned_date, email, book_id))

        if cursor.rowcount == 0:
            return jsonify({'error': 'No matching borrowed book found or book already returned'}), 404

        cursor.execute('''
            UPDATE Books
            SET rating = ?, review = ?, available = available + 1
            WHERE id = ?
        ''', (rating, review, book_id))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({'message': 'Book returned successfully'}), 201

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Error updating data'}), 500

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
    
@app.route('/crazy_admin_audit', methods=['POST'])
def save_admin_audit():
    create_admin_audit()
    print("I am trying to save the admin auditing information")
    email = request.json.get('email')
    approved_date = request.json.get('approved_date')
    approved_admin_email = request.json.get('approved_admin_email')
    approved_status = request.json.get('approved_status')

    if not email or not approved_date or not approved_admin_email:
        return jsonify({'error': 'No data provided'}), 400

    try:
        connect = connection()
        cursor = connect.cursor()
        cursor.execute('INSERT INTO Admin_Auditing (email, approved_date, approved_admin_email, approved_status) VALUES (?, ?, ?, ?)', (email, approved_date, approved_admin_email, approved_status))
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
create_admin_audit()

if __name__ == '__main__':
    create_books()  # Call create_books() only if running this script directly
    #sales_table()   # Call sales_table() only if running this script directly
    app.run(port=5000)
