import streamlit as st
import server
import sqlite3
import pandas as pd

def display():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Title, affiliation, interest, email, request_date FROM pending_request where email=?",(st.session_state.email,))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    if rows:
        st.write(f"{first_name} {last_name}, the following book requests are being processed:")
        df = pd.DataFrame(rows, columns=columns)
        df = st.data_editor(df, num_rows="dynamic")
        st.write("Please wait for a confirmation from the Librarian. Thank you!")
    else:
        st.write("You currently do not have any book requests.")
     

    conn.close()

if "email" in st.session_state and 'first_name' in st.session_state and 'last_name' in st.session_state:
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    display()
else:
    st.write("<a href='registration'>Please sign in</a>", unsafe_allow_html=True)