import streamlit as st
import requests
from string import punctuation
import server
import sqlite3


st.title("Registration Page")

first_name = st.text_input('Enter First Name:')
last_name = st.text_input('Enter Last Name:')
profile_picture = st.text_area('Upload profile picture:')
address = st.text_area('Enter address:')
phone = st.text_input('Enter phone number:')
email = st.text_input('Enter email:')
password = st.text_input('Create password:')


#forgotten password

def checkEmail(email):
    hasAt = '@' in email
    hasDot = '.' in email
    isValid = hasAt and hasDot and email.index('@') < email.rindex('.')
    return isValid

def checkPassword(password):
    specialKey = any(char in punctuation for char in password)
    hasNumbers = any(char.isdigit() for char in password)
    lengthValid = len(password)>=8
    
    if specialKey and lengthValid and hasNumbers:
        return True, ""
    elif not specialKey:
        return False, "Please include a special symbol" 
    elif not lengthValid:
        return False, "Please increase length to atleast 8 characters"
    elif not hasNumbers:
        return False, "Please add a number"
    
def user_exists(email):
    try:
        connect = server.connection()
        cursor = connect.cursor()
        query = 'SELECT email FROM User where email=?'
        cursor.execute(query, (email,))
        emails = cursor.fetchone()
        cursor.close()
        connect.close()

        if emails is not None:
            return True, emails
        else:
            return False, "should add user"
    except sqlite3.Error as e:
        print(e.errno())
        return False, "error"


if st.button('Submit'):
    
    if checkEmail(email):
        isPasswordValid, password_message = checkPassword(password)
        userExists, email_message = user_exists(email)
        if not userExists:
            if isPasswordValid:
                response = requests.post('http://127.0.0.1:5000/crazy_user', json={'first_name': first_name, 'last_name': last_name, 'address': address, 'phone': phone, 'email': email, 'password':password, 'profile_picture': profile_picture})
                if response.status_code == 201:
                    st.success('Account Created!')
                else:
                    st.error("Account not created succesfully :(")
            else:
                    st.error(password_message)
        else:
            st.error(f"{email_message} already registered, please login")
    else:
        st.error("Invalid email format")


