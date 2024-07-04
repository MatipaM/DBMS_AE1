import streamlit as st
import requests
from string import punctuation
import sqlite3
import server
from InfoManager import InfoManager
import bcrypt
import html
#import phonenumbers

st.title("Registration Page")

first_name = st.text_input('Enter First Name:')
last_name = st.text_input('Enter Last Name:')
profile_picture = st.text_area('Upload profile picture:')
# profile_picture = st.file_uploader('Upload profile picture:')
street = st.text_area('Enter Street:')
city = st.text_area('Enter City:')
postal_code = st.text_area('Enter postal code:', max_chars=7)
country = st.text_area('Enter country:')
phone = st.text_input('Enter phone number:', value='+44', max_chars=13, placeholder="+447588720903") #can only take UK numbers
affiliation = st.selectbox('Are you a: ', ('student', 'librarian', 'staff', 'administrator'))
email = st.text_input('Enter email: ', value=f"{first_name.lower()}{last_name.lower()}@{affiliation}.com")
password = st.text_input('Create password:', type='password')

hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

def checkEmail():
    hasAt = '@' in email
    hasDot = '.' in email
    isValid = hasAt and hasDot and email.index('@') < email.rindex('.')

    if isValid:
        return isValid, 'http://127.0.0.1:5000/crazy_user'
    else:
        return isValid, "Not a valid email"

#not working
def checkNames():
    firstValid = not (any(char.isdigit() for char in first_name))
    lastValid = not (any(char.isdigit() for char in last_name))

    firstLenValid = len(first_name)>1
    lastLenValid = len(first_name)>1

    if firstValid and lastValid and firstLenValid and lastLenValid:
        return True, ""
    elif not firstValid or not lastValid:
        return False, "Names must not contain any digits"
    elif not firstLenValid or not lastLenValid:
        return False, "Names must be longer than one character"

def checkPhoneNumber():
    isNumeric = phone[1:].strip().isnumeric()
    lengthValid = len(phone)==13
    startsZero = str(phone).startswith("+44")

    if isNumeric and lengthValid and startsZero:
        return True, ""
    elif not isNumeric:
        return False, "Phone number can only contain numbers"
    elif not lengthValid:
        return False, "Phone must contain eactly 11 numbers"
    elif not startsZero:
        return False, "Phone number must be a local UK number starting with 0"
    

def checkPassword():
    specialKey = any(char in punctuation for char in password)
    hasNumbers = any(char.isdigit() for char in password)
    lengthValid = len(password)>=8
    
    if specialKey and lengthValid and hasNumbers:
        return True, ""
    elif not specialKey:
        return False, "Password need to include a special symbol" 
    elif not lengthValid:
        return False, "Password length needs to be atleast 8 characters"
    elif not hasNumbers:
        return False, "Password needs a number"
    
def checkPostal():
    postalValid = len(postal_code)>=5 and len(postal_code)<=7

    if postalValid:
        return True,""
    else:
        return False, "Postal code must be between 5 and 7 letters"
    
def user_exists():
    try:
        connect = server.connection()
        cursor = connect.cursor()
        query = f'SELECT email FROM user where email=?'
        cursor.execute(query, (email,))
        emails = cursor.fetchone()
        cursor.close()
        connect.close()

        if emails is not None:
            return True, emails
        else:
            return False, "should add user"
    except sqlite3.Error as e:
        print(e)
        return False, "error"

address = f"{street}, {city}, {country}, {postal_code}"
user_type = email[email.index("@")+1: email.index(".com")]

if st.button('Submit'):
    emailValid, email_route = checkEmail()
    if emailValid:
        isPasswordValid, password_message = checkPassword()
        userExists, email_message = user_exists()
        phoneValid, phone_message = checkPhoneNumber()
        namesValid, name_message = checkNames()
        postalValid, postal_message = checkPostal()
        if namesValid:
            if phoneValid:
                if postalValid:
                    if not userExists:
                        if isPasswordValid:
                            response = requests.post(email_route, json={'first_name': html.escape(first_name), 'last_name': html.escape(last_name), 'address': html.escape(address), 'affiliation': html.escape(affiliation), 'phone': html.escape(phone), 'email': html.escape(email), 'password':html.escape(hashed_password), 'profile_picture': html.escape(profile_picture)})
                            if response.status_code == 201:
                                st.success('Registered successfully!')
                                if 'email' not in st.session_state:
                                    st.session_state.email = email
                                    
                                if 'first_name' not in st.session_state:
                                    st.session_state.first_name = first_name.capitalize()

                                if 'last_name' not in st.session_state:
                                    st.session_state.last_name = last_name.capitalize()

                                if 'user_type' not in st.session_state:
                                    st.session_state.user_type = user_type

                                if 'affiliation' not in st.session_state:
                                    st.session_state.affiliation = affiliation

                                for idx, user_page_array in enumerate(InfoManager().get_instance().user_pages_arrays):
                                    if user_page_array not in st.session_state:
                                        if affiliation==InfoManager().get_instance().users[idx]:
                                            st.session_state.user_page_array = InfoManager().get_instance().getPages(idx)
                                            print(st.session_state.user_page_array)
                    
                                                               
                                if affiliation == "administrator":
                                    response2 = requests.post('http://127.0.0.1:5000/crazy_admin_audit', json={'email': email, 'approved_date': "null", 'approved_admin_email': "null", "approved_status": "False"})
                                    st.session_state.user_page_array = InfoManager().get_instance().getPages(1)

                                    
                            else:
                                st.error("Account not created succesfully :(")
                        else:
                            st.error(password_message)
                    else:
                        st.error(f"{email_message} already registered, please login")
                else:
                    st.error(postal_message)
            else:
                st.error(phone_message)
        else:
            st.error(name_message)
    else:
        st.error(email_route)


