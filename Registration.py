import streamlit as st
import requests


st.title("Registration Page")

first_name = st.text_input('Enter First Name:')
last_name = st.text_input('Enter Last Name:')
profile_picture = st.text_area('Upload profile picture:')
address = st.text_area('Enter address:')
phone = st.text_input('Enter phone number:')
email = st.text_input('Enter email:')
password = st.text_input('Create password:')


if st.button('Submit'):
    response = requests.post('http://127.0.0.1:5000/crazy_user', json={'first_name': first_name, 'last_name': last_name, 'address': address, 'phone': phone, 'email': email, 'password':password, 'profile_picture': profile_picture})
    if response.status_code == 201:
        st.success('Account Created!')
    else:
        st.error('Failed to create User account')