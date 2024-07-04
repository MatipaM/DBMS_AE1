import streamlit as st
import requests
import datetime
import sqlite3
import pandas as pd
import os
from InfoManager import InfoManager

def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    st.title("Book Sales Section")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sales s LEFT JOIN Books b ON s.BookID = b.id WHERE date IS NULL")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    #this is probably a stupid way to do it but it works, anyways please make it better if you can
    rows = [list(row) for row in rows]
    for row in rows:
        if row[3] is None:
            row[3] = 20

    #st.write(rows)

    if rows:
        df = [(row[0], row[1], row[2], f'£{row[3]}', row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17]) for row in rows]
        df = pd.DataFrame(df, columns=columns)
        df['Select'] = False
        df = st.data_editor(df, num_rows="dynamic")
    else:
        st.write("No book for sale at this time.")

    if st.button("Purchase"):
        purchased_books = df[df['Select'] == True]

        for index, row in purchased_books.iterrows():
            cursor.execute(
                "UPDATE Sales SET date = ? WHERE BookID = ?",
                (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), row['BookID'])
            )
        conn.commit()
        conn.close()

        st.write("Redirecting to payment page...")
        st.switch_page("pages/payment.py")

        df = df[df['Select'] == False]


    InfoManager().get_instance().logout()

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
