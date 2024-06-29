import random
import streamlit as st
import requests

def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    st.title("Let's submit some books for the Library!")

    id = random.randint(1, 100);
    title = st.text_area('Enter title:')
    author = st.text_area('Enter Author:')
    publisher = st.text_area('Enter Publisher:')
    year_purchased = st.text_area('Enter Year purchased:')
    year_published = st.text_area('Enter Year published:')
    description = st.text_area('Enter description:')
    secondary_title = st.text_area('Enter secondary title:')
    version = st.text_area('Enter version:')
    quantity = st.number_input('Enter number of books: ', min_value=1)
    price = st.number_input('Enter re-sale price of book')
    available = "TORENT"  # Default value for testing
    review = ""
    rating = ""

    if st.button('Submit'):
        payload = {

            'title': title,
            'author': author,
            'publisher': publisher,
            'year_purchased': year_purchased,
            'year_published': year_published,
            'description': description,
            'secondary_title': secondary_title,
            'version': version,
            'quantity': quantity,
            'price': price,
            'available': available,  # Fixed typo here
            'review': review,
            'rating': rating
        }

        response = requests.post('http://127.0.0.1:5000/crazy_books', json=payload)

        if response.status_code == 201:
            st.success('Books submitted!')
        else:
            st.error(f'Failed to submit books: {response.status_code}')

if "email" in st.session_state and 'first_name' in st.session_state and 'last_name' in st.session_state:
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    if "librarian" in email:
        display()
    else:
        st.error(f"{first_name} {last_name}, you are not authorised to view this page.")
else:
    st.write("<a href='registration'>Please sign in</a>", unsafe_allow_html=True)
