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
        cursor.execute('INSERT INTO Books (title, author, publisher, description, secondary_title, version, year_purchased) VALUES (?, ?, ?, ?, ?, ?, ?)', (title, author, publisher, description, secondary_title, version, year_purchased))
        connect.commit()
        cursor.close()
        connect.close()
        return jsonify({'message': 'Data saved'}), 201
    except Error as e:
        print(e)
        return jsonify({'error': 'Error saving data'}), 500
    

# USER TABLE

# def save_user():
#     title = request.json.get('first_name')
#     author = request.json.get('last_name')
#     publisher = request.json.get('profile_picture')
#     description = request.json.get('description')  
#     secondary_title = request.json.get('secondary_title')
#     version = request.json.get('publisher')
#     year_purchased= request.json.get('year_purchased')  

#     if not title or not author or not publisher or not description or not secondary_title or not version or not year_purchased:
#         return jsonify({'error': 'No data provided'}), 400

#     try:
#         connect = connection()
#         cursor = connect.cursor()
#         cursor.execute('INSERT INTO Books (title, author, publisher, description, secondary_title, version, year_purchased) VALUES (?, ?, ?, ?, ?, ?, ?)', (title, author, publisher, description, secondary_title, version, year_purchased))
#         connect.commit()
#         cursor.close()
#         connect.close()
#         return jsonify({'message': 'Data saved'}), 201
#     except Error as e:
#         print(e)
#         return jsonify({'error': 'Error saving data'}), 500
    
if __name__ == '__main__':
    app.run(port=5000)
