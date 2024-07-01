import streamlit as st
import server
import sqlite3
import pandas as pd
import os
from InfoManager import InfoManager



def display():
    st.title(f"{first_name} {last_name}'s Home Page")
    st.write("Welcome to the Library Management System")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT Title, affiliation, interest, email, request_date FROM pending_request where email=?",(st.session_state.email,))
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    if rows:
        st.write(f"{first_name} {last_name}, the following book requests are being processed:")
        df = pd.DataFrame(rows, columns=columns)
        df = st.data_editor(df, num_rows="dynamic")
        st.write("Please wait for a confirmation from the Librarian. Thank you!")
    else:
        st.write("You currently do not have any book requests.")

    if st.button("logout"):
        if st.session_state.first_name is not "default_first_name":
            print("not default user")
            for key in st.session_state.keys():
                del st.session_state[key]
                InfoManager().get_instance().loginDefault()
                st.experimental_rerun()

    conn.close()

current_file_name = os.path.basename(__file__)

if "email" in st.session_state and 'first_name' in st.session_state and 'last_name' in st.session_state:
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            if current_file_name[:-3] in InfoManager().get_instance().getPages(idx):
                display()
            else:
                st.error(f"{first_name} {last_name}, you are not authorised to view this page.")
else:
    st.session_state.first_name = InfoManager().default_user["first_name"]
    st.session_state.last_name = InfoManager().default_user["last_name"]
    st.session_state.email = InfoManager().default_user["email"]
    st.session_state.affiliation = InfoManager().default_user["affiliation"]
    display()

if 'disapproval_reasons' in st.session_state:
    reasons = st.session_state.disapproval_reasons
    for reason in reasons:
        st.write(reason)

