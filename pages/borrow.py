import streamlit as st
import requests
from datetime import datetime


st.title("Let's Borrow Book")

email = st.text_input('Email:')
book_title = st.text_input('Book Title:')
affiliation = st.text_input('Affiliation:')
interest = st.text_input('Book Interest:')
date_borrowed = st.date_input('Date Borrowed', datetime.today())

if st.button('Submit'):
    date_borrowed = date_borrowed.strftime('%Y-%m-%d')
    response = requests.post('http://127.0.0.1:5000/crazy_borrow', json={'eamil': email, 'book_title': book_title, 'date_borrowed': date_borrowed, 'affiliation': affiliation, 'interest': interest})
    st.switch_page("pages/wait.py")
    if response.status_code == 201:
        st.success('Books submitted!')
    else:
        st.error('Failed to submit books')