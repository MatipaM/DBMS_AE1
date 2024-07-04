import streamlit as st
import requests
from InfoManager import InfoManager
import os
import html
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
        response = requests.post('http://127.0.0.1:5000/crazy_books', json={'title': html.escape(title), 'author': html.escape(author), 'publisher': html.escape(publisher), 'year_purchased': html.escape(year_purchased), 'description': html.escape(description), 'secondary_title':html.escape(secondary_title), 'version':html.escape(version), 'quantity': html.escape(quantity)})
        if response.status_code == 201:
            st.success('Books submitted!')
        else:
            st.error('Failed to submit books')

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

    