import streamlit as st
import requests
from string import punctuation
import server
import sqlite3
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
email = st.text_input('Enter email (either @student.com, @staff.com, @librarian.com or @administrator.com): ', value=f"{first_name.lower()}{last_name.lower()}@student.com")
password = st.text_input('Create password:', type='password')


def checkEmail():
    hasAt = '@' in email
    hasDot = '.' in email
    isValid = hasAt and hasDot and email.index('@') < email.rindex('.')

    if "@student" in email:
        return isValid, 'http://127.0.0.1:5000/crazy_student', 'student', ""
    elif "@administrator" in email:
        return isValid, 'http://127.0.0.1:5000/crazy_administrator', 'administrator', ""
    elif "@librarian" in email:
        return isValid, 'http://127.0.0.1:5000/crazy_librarian', 'librarian', ""
    elif "@staff" in email:
        return isValid, 'http://127.0.0.1:5000/crazy_staff', 'staff', ""
    else:
        return False, 'http://127.0.0.1:5000/crazy_user', 'user', "Please use a @student, @administrator, @librarian or @staff email"

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
    isNumeric = phone[-12].strip().isnumeric()
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
    
def user_exists(table_name):
    try:
        connect = server.connection()
        cursor = connect.cursor()
        query = f'SELECT email FROM {table_name} where email=?'
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

# if st.button('Submit'):
if st.write("<a href='request_book'>Submit</a>", unsafe_allow_html=True):
    emailValid, email_route, table_name, email_error_message = checkEmail()
    if emailValid:
        isPasswordValid, password_message = checkPassword()
        userExists, email_message = user_exists(table_name)
        phoneValid, phone_message = checkPhoneNumber()
        namesValid, name_message = checkNames()
        postalValid, postal_message = checkPostal()
        if namesValid:
            if phoneValid:
                if postalValid:
                    if not userExists:
                        if isPasswordValid:
                            response = requests.post(email_route, json={'first_name': first_name, 'last_name': last_name, 'address': address, 'phone': phone, 'email': email, 'password':password, 'profile_picture': profile_picture})
                            if response.status_code == 201:
                                st.success('Account Created!')
                                if 'email' not in st.session_state:
                                    st.session_state.email = email
                                
                                if 'first_name' not in st.session_state:
                                    st.session_state.first_name = first_name

                                if 'last_name' not in st.session_state:
                                    st.session_state.last_name = last_name

                                if 'user_type' not in st.session_state:
                                    st.session_state.user_type = user_type
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
        st.error(email_error_message)


