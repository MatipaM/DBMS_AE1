import streamlit as st
import requests

st.title("Let's submit some books for the Librarian!")

title = st.text_area('Enter title:')
author = st.text_area('Enter Author:')
publisher = st.text_area('Enter Publisher:')
year_purchased = st.text_area('Enter Year Published:')
description = st.text_area('Enter description:')
secondary_title = st.text_area('Enter secondary title:')
version = st.text_area('Enter version:')


if st.button('Submit'):
    response = requests.post('http://127.0.0.1:5000/crazy_books', json={'title': title, 'author': author, 'publisher': publisher, 'year_purchased': year_purchased, 'description': description, 'secondary_title':secondary_title, version:'version'})
    if response.status_code == 201:
        st.success('Books submitted!')
    else:
        st.error('Failed to submit books')