import streamlit as st
import sqlite3
import pandas as pd
import requests
import datetime
import server

def display():
    st.write("Here are the books available for borrowing:")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, author, publisher, description, version FROM Books")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    if rows:
        df = pd.DataFrame(rows, columns=columns)
        df['Select'] = False
        df = st.data_editor(df, num_rows="dynamic")
    else:
        st.write("No Book Available.")

    conn.close()

    interest = st.text_input('Book Interests:')
    request_date = st.date_input('Request Date:', datetime.datetime.now())

    if st.button('Borrow Selected Books'):
        request_date_str = request_date.strftime('%Y-%m-%d %H:%M:%S')
        selected_books = df[df['Select'] == True]
        if selected_books.empty:
            st.warning('Please select at least one book to borrow.')
        else:
            selected_books['interest'] = interest
            books = selected_books.to_dict('records')
            for book in books:
                book['id'] = int(book['id'])
            #st.write("Selected Books:")
            #st.write(books)
            #st.write("Request Data:")
            request_data = {'email': email, 'date_request': request_date_str, 'books': books}
            #st.write(request_data)
            
            response = requests.post('http://127.0.0.1:5000/crazy_borrow', json=request_data)
            try:
                response.json()
            except requests.exceptions.JSONDecodeError as e:
                str(e)
                response.text
            if response.status_code == 201:
                st.success('Book requested!')
            else:
                st.error('Failed to submit books')

if 'first_name' in st.session_state and 'last_name' in st.session_state and 'email' in st.session_state and 'user_type' in st.session_state:
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    email = st.session_state.email
    affiliation = st.session_state.user_type
    st.header(f"Welcome, {first_name} {last_name}!")
    display()
else:
    st.write("<a href='registration'>Please sign in to view this page</a>", unsafe_allow_html=True)