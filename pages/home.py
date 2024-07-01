import streamlit as st
import server
import sqlite3
import pandas as pd
import os
from InfoManager import InfoManager



def display():
    st.header(f"{first_name} {last_name}'s Home Page")
    st.title("Welcome to the Library Management System")

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

    InfoManager().get_instance().logout()

    conn.close()

current_file_name = os.path.basename(__file__)

if hasattr(st.session_state, "first_name"):
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    affiliation = st.session_state.affiliation

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            print("affiliation", st.session_state.affiliation)
            print(current_file_name, InfoManager().get_instance().getPages(idx))
            if current_file_name[:-3] in InfoManager().get_instance().getPages(idx):
                display()
            else:
                st.error(f"{first_name} {last_name}, {affiliation}'s are not authorised to view this page.")
                InfoManager().get_instance().logout()
else:
    InfoManager().get_instance().loginDefault()
    display()

