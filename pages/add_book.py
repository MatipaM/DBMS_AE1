import streamlit as st
import requests
from InfoManager import InfoManager
import os
# import server


def display():
    # server.create_books() 
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    st.title("Let's submit some books for the Library!")

    title = st.text_area('Enter title:')
    author = st.text_area('Enter Author:')
    publisher = st.text_area('Enter Publisher:')
    year_purchased = st.text_area('Enter Year Published:')
    description = st.text_area('Enter description:')
    secondary_title = st.text_area('Enter secondary title:')
    version = st.text_area('Enter version:')
    quantity = st.number_input('Enter number of books: ', min_value= 1)


    if st.button('Submit'):
        response = requests.post('http://127.0.0.1:5000/crazy_books', json={'title': title, 'author': author, 'publisher': publisher, 'year_purchased': year_purchased, 'description': description, 'secondary_title':secondary_title, 'version':version, 'quantity': quantity})
        if response.status_code == 201:
            st.success('Books submitted!')
        else:
            st.error('Failed to submit books')

    if st.button("logout"):
        if st.session_state.first_name is not "default_first_name":
            print("not default user")
            for key in st.session_state.keys():
                del st.session_state[key]
                InfoManager().get_instance().loginDefault()
                st.experimental_rerun()

current_file_name = os.path.basename(__file__)

print(st.session_state.email, st.session_state.first_name);

if st.session_state.email is not None and 'first_name' in st.session_state and 'last_name' in st.session_state:
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            print(current_file_name, InfoManager().get_instance().getPages(idx))
            if current_file_name[:-3] in InfoManager().get_instance().getPages(idx):
                display()
            else:
                st.error(f"{first_name} {last_name}, you are not authorised to view this page.")
else:
    InfoManager().get_instance().loginDefault()
    display()
    