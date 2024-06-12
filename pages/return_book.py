import streamlit as st
import requests
from datetime import datetime

# Book Return Page
def display():
    st.title("Let's Return Book")



    title = st.text_input('Title:')
    return_date =  st.date_input('Return Date:', datetime.today())
    rating = st.number_input('Rating:', min_value = 1, max_value=5)
    review = st.text_area('Review:')

    if st.button('Submit'):
        return_date_str = return_date.strftime('%Y-%m-%d')
        response = requests.post("/crazy_return", json={'email': email, 'title': title, 'return_date': return_date_str, 'rating': rating, 'review': review})

        if response.status_code == 201:
            st.success('Book returned!')
            st.switch_page("pages/wait.py")
        else:
            st.error('Failed to return book')

if 'first_name' in st.session_state and 'last_name' in st.session_state and 'email' in st.session_state and 'user_type' in st.session_state:
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    email = st.session_state.email
    affiliation = st.session_state.user_type
    st.header(f"Welcome, {first_name} {last_name}!")
    display()
else:
    st.write("<a href='registration'>Please sign in to view this page</a>", unsafe_allow_html=True)

