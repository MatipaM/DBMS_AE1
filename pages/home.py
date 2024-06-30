import streamlit as st
import server
import sqlite3
import pandas as pd

def display():
    st.title(f"{first_name} {last_name}'s Home Page")
    st.write("Welcome to the Library Management System")

    if st.button("View Books for Sale and Purchase"):
        st.switch_page("pages/user_sales.py")
    if st.button("View Books for Request"):
        st.switch_page("pages/request_book.py")
    if st.button("View Books for Return"):
        st.switch_page("pages/return_book.py")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT title, affiliation, interest, email, date_request FROM Pending_Request WHERE email = ?", (st.session_state.email,))
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
    st.write("<a href='registration'>Please sign in to see any pending book requests</a>", unsafe_allow_html=True)

if 'disapproval_reasons' in st.session_state:
    reasons = st.session_state.disapproval_reasons
    for reason in reasons:
        st.write(reason)