import streamlit as st
import base64
import os
import server
import sqlite3
import requests

# Function to add background image
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
        }}
        .header {{
            font-size: 50px; /* Font size */
            color: #4CAF50; /* Font color */
            font-weight: bold; /* Bold text */
            font-family: 'time New Roman', sans-serif; /* Font type */
        }}
        .input-container {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .input-label {{
            font-size: 16px; /* Font size */
            color: black; /* Font color */
            font-weight: bold; /* Bold text */
            font-family: 'Arial', sans-serif; /* Font type */
            margin-right: 10px; /* Space between label and input */
            width: 100px; /* Fixed width for labels */
        }}
        .input-field {{
            flex: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Path to your image
current_dir = os.getcwd()
image_path = os.path.join(current_dir, "pages/library1.jpg")
# image_path = "library1.jpg"
add_bg_from_local(image_path)

# Header with custom class for styling
st.title('Library Management System')

# Email input with label
email = st.text_input('Please enter email:')
# Password input with label
password = st.text_input("Please enter password: ")

def user_exists(table_name):
    try:
        connect = server.connection()
        cursor = connect.cursor()
        query = f'SELECT email, password, first_name, last_name FROM {table_name} where email=?'
        cursor.execute(query, (email,))
        db_email, db_password, db_first_name, db_last_name = cursor.fetchone()
        cursor.close()
        connect.close()

        if db_email == email:
            if password == db_password:
                return True, "Login successful", db_first_name, db_last_name
            else:
                return False, "incorrect password", "", ""
        else:
            return False, "Email is not associated with an account, Please register", "", ""
    except sqlite3.Error as e:
        print(e)
        return False, "error", "", ""
    

def checkEmail():
    if "@student" in email:
        return True,'student', 'http://127.0.0.1:5000/crazy_student'
    elif "@administrator" in email:
        return True, 'administrator', 'http://127.0.0.1:5000/crazy_administrator'
    elif "@librarian" in email:
        return True,'librarian', 'http://127.0.0.1:5000/crazy_librarian'
    elif "@staff" in email:
        return True, 'staff', 'http://127.0.0.1:5000/crazy_staff'
    else:
        return False, 'invalid email', ""

if st.button('Login'):
    emailValid, table_name, email_route = checkEmail()
    userExists, email_message, first_name, last_name = user_exists(table_name) #if user exsists and password correct
    if userExists:
        st.success('Logged in successfully!')
        if 'email' not in st.session_state:
            st.session_state.email = email
                                
        if 'first_name' not in st.session_state:
            st.session_state.first_name = first_name

        if 'last_name' not in st.session_state:
            st.session_state.last_name = last_name

        if 'user_type' not in st.session_state:
            st.session_state.user_type = table_name
        else:
            st.error("Account not created succesfully :(")
    else:
        st.error(email_message)

 
