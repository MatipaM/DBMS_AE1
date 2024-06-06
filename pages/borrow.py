import streamlit as st
import requests
from datetime import datetime


st.title("Let's Borrow Book")

user_id = st.text_input('Enter User ID:')
book_title = st.text_input('Enter Book Title:')
date_borrowed = st.date_input('Date Borrowed', datetime.today())

if st.button('Submit'):
    response = requests.post('http://127.0.0.1:5000/crazy_borrow', json={'user_id': user_id, 'book_title': book_title, 'date_borrowed': date_borrowed})
    if response.status_code == 201:
        st.success('Books submitted!')
    else:
        st.error('Failed to submit books')