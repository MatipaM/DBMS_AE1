import streamlit as st
import requests
from datetime import datetime
from InfoManager import InfoManager
import os
import json

# Book Return Page
def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    st.title("Let's Return Book")

    title = st.text_input('Title:')
    return_date = st.date_input('Return Date:', datetime.today())
    rating = st.number_input('Rating:', min_value=1, max_value=5)
    review = st.text_area('Review:')

    if st.button('Submit'):
        return_date_str = return_date.strftime('%Y-%m-%d')
        data = {
            'email': st.session_state.email,
            'title': title,
            'returned_date': return_date_str,
            'rating': rating,
            'review': review
        }
        #st.write("Sending data:", json.dumps(data, indent=2)) 
        try:
            response = requests.post("http://127.0.0.1:5000/crazy_return", json=data)
            
            # st.write(f"Response status code: {response.status_code}")
            # st.write(f"Response content: {response.text}") 
            
            if response.status_code == 201:
                st.success('Book returned!')
                st.switch_page("pages/wait.py")
            else:
                try:
                    error_message = response.json().get("error", "Unknown error")
                except ValueError:
                    error_message = response.text if response.text else "Unknown error"
                st.error(f'Failed to return book: {error_message}')
                
        except requests.RequestException as e:
            st.error(f'Failed to connect to the server: {str(e)}')

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

