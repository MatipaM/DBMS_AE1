import streamlit as st
import requests
from datetime import datetime
import sqlite3
import pandas as pd

st.title("Book Sales Section")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM Books GROUP BY Title, Author, Publisher, Description, Year_Purchased, Secondary_Title, Version HAVING COUNT(*) > 1")
books_rows = cursor.fetchall()

for row in books_rows:
    cursor.execute("INSERT INTO Sales (Title, Author, Publisher, Description, Year_Purchased, Secondary_Title, Version, Price) VALUES (?, ?, ?, ?, ?, ?, ?, NULL)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
    cursor.execute("DELETE FROM Books WHERE Title = ? AND Author = ? AND Publisher = ? AND Description = ? AND Year_Purchased = ? AND Secondary_Title = ? AND Version = ?", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

conn.commit()

cursor.execute("SELECT Title, Author, Publisher, Price FROM Sales")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]
conn.close()

if rows:
    df = [(row[0], row[1], row[2], f'£{row[3]}') for row in rows]
    df = pd.DataFrame(df, columns=columns)
    df['Select'] = False
    df = st.data_editor(df, num_rows="dynamic")
else:
    st.write("No book for sale at this time.")