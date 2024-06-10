import streamlit as st
import requests
from datetime import datetime

# Book Return Page


if 'email' in st.session_state and 'user_type' in st.session_state:
    email = st.session_state.email
    affiliation = st.session_state.user_type

else:
    st.write("<a href='registration'>Please sign in</a>", unsafe_allow_html=True)

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

