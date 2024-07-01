import streamlit as st
import sqlite3
import pandas as pd
import requests
from datetime import datetime
from InfoManager import InfoManager
import os


def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    st.title("Available Books!")

    st.write("Here are the books available for borrowing:")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Title, Secondary_Title, Author, Publisher, Description, Version FROM Books")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    if rows:
        df = pd.DataFrame(rows, columns=columns)
        df['Select'] = False
        df = st.data_editor(df, num_rows="dynamic")
    else:
        st.write("No Book Available.")

    conn.close()



    st.title("Want to Borrow Book?")


    interest = st.text_input('Book Interests:')
    request_date =  st.date_input('Request Date:', datetime.today())

    if st.button('Borrow Selected Books'):
        request_date_str = request_date.strftime('%Y-%m-%d')
        selected_books = df[df['Select'] == True]
        if selected_books.empty:
            st.warning('Please select at least one book to borrow.')
        else:
            selected_books = selected_books.drop(columns=['Select'])
            title = ', '.join(selected_books['Title'].tolist())
            st.write(f'Borrowing books: {title, request_date_str, affiliation, interest, email}')

        response = requests.post('http://127.0.0.1:5000/crazy_borrow', json={'email': email, 'title': title, 'affiliation': affiliation, 'interest': interest, 'request_date': request_date_str})
        if response.status_code == 201:
            st.success('Book requested!')
            #st.switch_page("pages/wait.py")
        else:
            st.error('Failed to submit books')

    InfoManager().get_instance().logout()

current_file_name = os.path.basename(__file__)


if hasattr(st.session_state, "first_name"):
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    affiliation = st.session_state.affiliation

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            print("affiliation", st.session_state.affiliation)
            print(current_file_name, InfoManager().get_instance().getPages(idx))
            if current_file_name[:-3] in InfoManager().get_instance().getPages(idx):
                display()
            else:
                st.error(f"{first_name} {last_name}, {affiliation}'s are not authorised to view this page.")
                InfoManager().get_instance().logout()
else:
    InfoManager().get_instance().loginDefault()
    display()