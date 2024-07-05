import streamlit as st
import server
import sqlite3
import pandas as pd
import os
from InfoManager import InfoManager

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

current_file_name = os.path.basename(__file__)

if hasattr(st.session_state, "first_name"):
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

#if 'approval_message' in st.session_state:
    #st.write(st.session_state.approval_message)

def email_exists(session_email):
    conn = sqlite3.connect('database.db')  
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM Book_records WHERE email=?", (session_email,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

session_email = st.session_state.get('email', '')

if email_exists(session_email):

    st.write("Please choose how you would like to receive your book:")
    choice = st.radio("Choose an option", ["Pick Up", "Posted"])
    token_amount = st.number_input("Enter the token amount", min_value=0, step=1)

    if st.button("Submit"):
        if token_amount > 0:
            st.session_state.approval_message = f"You have chosen {choice} and paid a token of {token_amount}."
            if choice == "Posted":
                st.session_state.approval_message += " Your book will be posted to you in 2 days. Thank you!"
            elif choice == "Pick Up":
                st.session_state.approval_message += " Your book will be ready for pick up tomorrow 9am. Thank you!"
        else:
            st.session_state.approval_message = f"You have chosen {choice} but did not pay the token."

        st.experimental_rerun()
    