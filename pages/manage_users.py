import streamlit as st
import pandas  as pd
from InfoManager import InfoManager
import os
import sqlite3
from datetime import datetime

def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    st.title("Manage users")

    st.write("Authenticate Adminstrators:")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # cursor.execute('''SELECT distinct Admin_Auditing.email as AdminEmail, User.first_name, User.last_name, User.affiliation
    #                FROM Admin_Auditing 
    #                JOIN User ON Admin_Auditing.Email = User.email 
    #                 ''')

    cursor.execute('''SELECT distinct User.email, first_name, last_name, affiliation, Admin_Auditing.approved_status
                   FROM User 
                   join Admin_Auditing on Admin_Auditing.email = User.email
                   Where User.email = Admin_Auditing.Email and Admin_Auditing.approved_status='False'
                    ''')

    columns = ['Email', 'First name', 'Last Name', 'Affiliation', 'Approved Status']

    rows = cursor.fetchall()

    df = pd.DataFrame(rows, columns=columns)
    df['Select'] = False
    table = st.data_editor(df, num_rows="dynamic")

    if st.button("Approve"):
        approved_requests = df[df['Select'] == True]

        for index, row in approved_requests.iterrows():
            cursor.execute(
                "INSERT INTO Admin_Auditing (email, approved_date, approved_admin_email, approved_status (?, ?, ?, ?)",
                (row['Email'], datetime.now().date(), st.session_state.email, "True")
            )


        conn.commit()
        conn.close()
        df = df[df['Select'] == False]
        df.drop(columns=['Select'], inplace=True)
        st.write("Approved!")
    elif st.button("Disapprove"):
        approved_requests = df[df['Select'] == True]

        for index, row in approved_requests.iterrows():
            cursor.execute(
            "UPDATE Admin_Auditing SET approved_date = ?, approved_admin_email = ?, approved_status = ? WHERE email = ?",
            (datetime.now().date(), st.session_state.email, "False", row['Email'])
        )

        conn.commit()
        conn.close()
        df = df[df['Select'] == False]
        df.drop(columns=['Select'], inplace=True)
        st.write("Disapproved!")

    st.title("Manage user Access")

    column_headings = ["Pages user has access to", "Approve"]
    buttons = []

    for a in range(4):
        pages_name = f"{InfoManager().get_instance().users[a]}_pages"
        pages_name=[]
        st.header(InfoManager().get_instance().users[a])
        buttons=[]
        for b in InfoManager().get_instance().project:
            new_select = st.checkbox(f"{InfoManager().get_instance().users[a]}: approve access to {b} page", value=any(b in page for page in InfoManager().get_instance().getPages(a)));
            buttons.append(new_select);
            if new_select:
                pages_name.append(f"{b}")


        print("pages_name", pages_name)
        InfoManager().user_pages_arrays[a] = pages_name

        pd.DataFrame({
            'Pages user has access to': InfoManager().project,
            'Approve': buttons
        })
        st.write(f"{InfoManager().get_instance().users[a]} has access to {pages_name}")
        InfoManager().get_instance().setPages(a, pages_name)

    InfoManager().get_instance().logout()

current_file_name = os.path.basename(__file__)

if hasattr(st.session_state, "first_name"):
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    affiliation = st.session_state.affiliation

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            if current_file_name[:-3] in InfoManager().get_instance().getPages(idx):
                display()
            else:
                st.error(f"{first_name} {last_name}, {affiliation}'s are not authorised to view this page.")
                InfoManager().get_instance().logout()
else:
    InfoManager().get_instance().loginDefault()
    display()

