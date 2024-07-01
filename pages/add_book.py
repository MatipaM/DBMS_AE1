import random
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
    year_purchased = st.text_area('Enter Year Purchased:')
    year_published = st.text_area('Enter Year Published:')
    description = st.text_area('Enter description:')
    secondary_title = st.text_area('Enter secondary title:')
    version = st.text_area('Enter version:')
    quantity = st.number_input('Enter number of books: ', min_value=1)
    available = st.number_input('Enter number of books available: ', min_value=1)
    rating = st.number_input('Enter rating: ', min_value=1, max_value=5)
    review = st.text_area('Enter review:')
    price = st.number_input('Enter price:', value=0.0)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('Submit'):
            data = {
                'title': title,
                'author': author,
                'publisher': publisher,
                'year_purchased': year_purchased,
                'year_published': year_published,
                'description': description,
                'secondary_title': secondary_title,
                'version': version,
                'quantity': quantity, 
                'available': available,
                'rating': rating,
                'price': price
            }

            if review:
                data['review'] = review

            response = requests.post('http://127.0.0.1:5000/crazy_books', json=data)
            if response.status_code == 201:
                st.success('Books submitted!')
            else:
                st.error(f'Failed to submit books: {response.status_code}')

    with col2:
        if st.button('Back to Home Page'):
            st.switch_page("pages/lib_review.py")
    
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
