import sqlite3
import pandas as pd
import streamlit as st
import pandas as pd

# Librarian Book Request Review
# 3 conditions: Returned all books, paid outstanding bills, and current student

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Pending_Request")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]
conn.close()

st.write("### Pending Book Requests")

if rows:
    df = pd.DataFrame(rows, columns=columns)
    df = st.data_editor(df, num_rows="dynamic")
else:
    st.write("No Book Requests.")