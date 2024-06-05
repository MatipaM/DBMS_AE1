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
    
if __name__ == '__main__':
    app.run(port=5000)