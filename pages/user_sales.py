import streamlit as st
import requests
from datetime import datetime
import sqlite3
import pandas as pd

st.title("Book Sales Section")

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM Books GROUP BY Title, Author, Publisher, Year_Purchased, Description, Secondary_Title, Version HAVING COUNT(*) > 1")
books_rows = cursor.fetchall()

for row in books_rows:
    cursor.execute("INSERT INTO Sales (Title, Author, Publisher, Description, Year_Purchased, Secondary_Title, Version, Price) VALUES (?, ?, ?, ?, ?, ?, ?, NULL)", (row[0], row[1], row[2], row[3], row[4], row[5], row[6]))

    cursor.execute("""
        WITH CTE AS (
            SELECT rowid,Title, Author, Publisher, Description, Year_Purchased, Secondary_Title, Version, ROW_NUMBER() OVER (PARTITION BY Title, Author, Publisher, Description, Year_Purchased, Secondary_Title, Version ORDER BY (SELECT NULL)) AS rn FROM Books)
        DELETE FROM Books
        WHERE rowid IN (SELECT rowid FROM CTE WHERE rn > 1 LIMIT 1); """)

conn.commit()

cursor.execute("SELECT Title, Author, Publisher, Price FROM Sales")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

#this is probably a stupid way to do it but it works, anyways please make it better if you can
rows = [list(row) for row in rows]
for row in rows:
    if row[3] is None:
        row[3] = 20

if rows:
    df = [(row[0], row[1], row[2], f'£{row[3]}') for row in rows]
    df = pd.DataFrame(df, columns=columns)
    df['Select'] = False
    df = st.data_editor(df, num_rows="dynamic")
else:
    st.write("No book for sale at this time.")

conn.close()

if st.button("Purchase"):
    purchased_books = df[df['Select'] == True]

    for index, row in purchased_books.iterrows():
        cursor.execute(
            "DELETE FROM Sales WHERE Title = ? AND Author = ? AND Publisher = ?",
            (row['Title'], row['Author'], row['Publisher'])
        )
        cursor.execute(
            "INSERT INTO Transaction (Price, Date, Title, Author) VALUES (?, ?, ?, ?)",
            (row['Price'], datetime.today().strftime('%Y-%m-%d'), row['Title'], row['Author'])
        )
    conn.commit()
    conn.close()

    st.write("Books purchased! It will be delivered to you soon.")
    df = df[df['Select'] == False]