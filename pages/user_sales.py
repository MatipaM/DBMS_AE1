import streamlit as st
import requests
from datetime import datetime
import sqlite3
import pandas as pd
import os
from InfoManager import InfoManager

def display():
    st.title("Book Sales Section")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Sales")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    #this is probably a stupid way to do it but it works, anyways please make it better if you can
    rows = [list(row) for row in rows]
    for row in rows:
        if row[3] is None:
            row[3] = 20

    if rows:
        df = [(row[0], row[1], row[2], f'£{row[3]}') for row in rows]
        df = pd.DataFrame(df, columns=columns)
        df['Select'] = False
        df = st.data_editor(df, num_rows="dynamic")
    else:
        st.write("No book for sale at this time.")

    if st.button("Purchase"):
        purchased_books = df[df['Select'] == True]

        for index, row in purchased_books.iterrows():
            cursor.execute(
                "DELETE FROM Sales WHERE SalesID = ? AND BookID = ? AND Year_Purchased = ? AND Price = ?",
                (row['SalesID'], row['BookID'], row['Year_Purchased'], row['Price'])
            )
            cursor.execute(
                "INSERT INTO `Transaction` (SalesID, Date) VALUES (?, ?)",
                (row['SalesID'], datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )

        conn.commit()
        conn.close()

        st.write("Redirecting to payment page...")
        st.switch_page("pages/payment.py")

        df = df[df['Select'] == False]

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