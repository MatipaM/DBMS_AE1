import streamlit as st
import requests

st.title("Let's submit some books for the Librarian!")

title = st.text_area('Enter title:')
author = st.text_area('Enter Author:')
if st.button('Submit'):
    response = requests.post('http://127.0.0.1:5000/crazy_books', json={'title': title, 'author': author})
    if response.status_code == 201:
        st.success('Books submitted!')
    else:
        st.error('Failed to submit books')