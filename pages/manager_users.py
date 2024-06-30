import streamlit as st
import pandas  as pd
from InfoManager import InfoManager

st.title("Manage users")

st.write("Authenticate Adminstrators")
st.write("Authenticate Students")
st.write("Authenticate staff")
st.write("Autennticate Librarians")
st.title("Manage user Access")

Project  = ["Registeration", "login", "add book", "Home", "lib review", "manage users","manager", "payment", "request book","return book","users sales"]
column_headings = ["Pages user has access to", "Approve"]
buttons = []

info = InfoManager()

positions = ["staff", "students", "administrator", "librarians"]
for a in range(4):
    pages_name = f"{positions[a]}_pages"
    pages_name=[]
    st.header(positions[a])
    buttons=[]
    for b in info.project:
        new_select = st.checkbox(f"{positions[a]}: approve access to {b} page");
        buttons.append(new_select);
        if new_select:
            pages_name.append(f"{b} page")

    pd.DataFrame({
        'Pages user has access to': Project,
        'Approve': buttons
    })
    st.write(f"{positions[a]} has access to {pages_name}")