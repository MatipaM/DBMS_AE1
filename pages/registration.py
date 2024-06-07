import streamlit as st
import requests
from string import punctuation
import server
import sqlite3
import phonenumbers


st.title("Registration Page")

first_name = st.text_input('Enter First Name:')
last_name = st.text_input('Enter Last Name:')
profile_picture = st.text_area('Upload profile picture:')
street = st.text_area('Enter Street:')
city = st.text_area('Enter City:')
postal_code = st.text_area('Enter postal code:')
country = st.text_area('Enter country:')
phone = st.text_input('Enter phone number:', max_chars=11, placeholder="01234567891") #can only take UK numbers
email = st.text_input('Enter email:')
password = st.text_input('Create password:', type='password')


#forgotten password

#not working
def checkPhoneNumber(phone):
    isNumeric = phone.isnumeric()
    lengthValid = len(phone)==11
    startsZero = str(phone).startswith("0")
    print(startsZero)

    if isNumeric and lengthValid and startsZero:
        print(isNumeric, lengthValid, startsZero)
        return True, ""
    elif not isNumeric:
        return False, "Phone number can only contain numbers"
    elif not lengthValid:
        return False, "Phone must contain eactly 11 numbers"
    elif not startsZero:
        return False, "Phone number must be a local UK number starting with 0"
    

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

address = f"{street}, {city}, {country}, {postal_code}"

if st.button('Submit'):
    
    if checkEmail(email):
        isPasswordValid, password_message = checkPassword(password)
        userExists, email_message = user_exists(email)
        phoneValid, phone_message = checkPhoneNumber(phone)
        if phoneValid:
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
            st.error(phone_message)
    else:
        st.error("Invalid email format")


