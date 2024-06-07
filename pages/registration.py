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
postal_code = st.text_area('Enter postal code:', max_chars=7)
country = st.text_area('Enter country:')
phone = st.text_input('Enter phone number:', max_chars=11, placeholder="01234567891") #can only take UK numbers
email = st.text_input('Enter email:')
password = st.text_input('Create password:', type='password')


#forgotten password

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
    isNumeric = phone.isnumeric()
    lengthValid = len(phone)==11
    startsZero = str(phone).startswith("0")

    if isNumeric and lengthValid and startsZero:
        return True, ""
    elif not isNumeric:
        return False, "Phone number can only contain numbers"
    elif not lengthValid:
        return False, "Phone must contain eactly 11 numbers"
    elif not startsZero:
        return False, "Phone number must be a local UK number starting with 0"
    

def checkEmail():
    hasAt = '@' in email
    hasDot = '.' in email
    isValid = hasAt and hasDot and email.index('@') < email.rindex('.')
    return isValid

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
    
    if checkEmail():
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
                    st.error(postal_message)
            else:
                st.error(phone_message)
        else:
            st.error(name_message)
    else:
        st.error("Invalid email format")


