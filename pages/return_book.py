import streamlit as st
import requests
from datetime import datetime
from InfoManager import InfoManager
import os

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

current_file_name = os.path.basename(__file__)

if "email" in st.session_state and 'first_name' in st.session_state and 'last_name' in st.session_state:
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name

    for idx,i in enumerate(InfoManager().users):
        if st.session_state.affiliation == i:
            print(current_file_name)
            if current_file_name in InfoManager().user_pages_arrays[idx]:
                display()
            else:
                st.error(f"{first_name} {last_name}, you are not authorised to view this page.")
else:
    st.session_state.first_name = InfoManager().default_user["first_name"]
    st.session_state.last_name = InfoManager().default_user["last_name"]
    st.session_state.email = InfoManager().default_user["email"]
    st.session_state.affiliation = InfoManager().default_user["affiliation"]
    display()

