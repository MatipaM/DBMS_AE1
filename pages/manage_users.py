import streamlit as st
import pandas  as pd
from InfoManager import InfoManager
import os

def display():
    st.title("Manage users")

    st.write("Authenticate Adminstrators")
    st.write("Authenticate Students")
    st.write("Authenticate staff")
    st.write("Autennticate Librarians")
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
                pages_name.append(f"{b} page")


        InfoManager().user_pages_arrays[a] = pages_name

        pd.DataFrame({
            'Pages user has access to': InfoManager().project,
            'Approve': buttons
        })
        st.write(f"{InfoManager().get_instance().users[a]} has access to {pages_name}")
        InfoManager().get_instance().setPages(a, pages_name)

current_file_name = os.path.basename(__file__)

if "email" in st.session_state and 'first_name' in st.session_state and 'last_name' in st.session_state:
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            print(current_file_name[:-3], InfoManager().get_instance().getPages(idx))
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