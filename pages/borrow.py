import streamlit as st
import requests
from datetime import datetime


st.title("Let's Borrow Book")

email = st.text_input('Email:')
book_title = st.text_input('Book Title:')
affiliation = st.text_input('Affiliation:')
interest = st.text_input('Book Interest:')
request_date =  st.date_input('Request Date:', datetime.today())

if st.button('Submit'):
    request_date_str = request_date.strftime('%Y-%m-%d')
    response = requests.post('http://127.0.0.1:5000/crazy_borrow', json={'email': email, 'book_title': book_title, 'request_date': request_date_str, 'affiliation': affiliation, 'interest': interest})
    if response.status_code == 201:
        st.success('Books submitted!')
        st.switch_page("pages/wait.py")
    else:
        st.error('Failed to submit books')