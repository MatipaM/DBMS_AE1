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
        conn.commit()
        cursor.close()
        conn.close()
        print("Book table created successfully")
    except Error as e:
        print(e)

def sales_table():
    sales_data = [
        ("1234", "6894", "1990", 20),
        ("2235", "7890", "1987", 19),
        ("3345", "8890", "2001", 39),
        ("1345", "8890", "2001", 39),
        ("3115", "2239", "2002", 15),
    ]
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
        conn.commit()

        for data in sales_data:
            cursor.execute('INSERT INTO Sales (BookID, SalesID, Year_Purchased, Price) VALUES (?, ?, ?, ?)', data)

        conn.commit()
        cursor.close()
        conn.close()
        print("Sales table created successfully")
    except sqlite3.Error as e:
        print(e)

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
    # Function implementation remains the same as in your original code
    pass

@app.route('/crazy_borrow', methods=['POST'])
def borrow_book():
    # Function implementation remains the same as in your original code
    pass

@app.route('/crazy_return', methods=['POST'])
def return_book():
    # Function implementation remains the same as in your original code
    pass

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
        cursor.execute('INSERT INTO Sales (BookID, SalesID, Year_Purchased, Price) VALUES (?, ?, ?, ?)', (book_id, sales_id, year_purchased, price))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500

if __name__ == '__main__':
    create_books()  # Call create_books() only if running this script directly
    sales_table()   # Call sales_table() only if running this script directly
    app.run(port=5000, debug=True)
