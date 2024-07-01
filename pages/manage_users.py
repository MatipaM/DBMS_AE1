import streamlit as st
import pandas  as pd
from InfoManager import InfoManager

st.title("Manage users")

st.write("Authenticate Adminstrators")
st.write("Authenticate Students")
st.write("Authenticate staff")
st.write("Autennticate Librarians")
st.title("Manage user Access")

column_headings = ["Pages user has access to", "Approve"]
buttons = []

for a in range(4):
    pages_name = f"{InfoManager().users[a]}_pages"
    pages_name=[]
    st.header(InfoManager().users[a])
    buttons=[]
    for b in InfoManager().project:
        new_select = st.checkbox(f"{InfoManager().users[a]}: approve access to {b} page", value=any(b in page for page in InfoManager().user_pages_arrays[a]));
        buttons.append(new_select);
        if new_select:
            pages_name.append(f"{b} page")

    InfoManager().user_pages_arrays[a] = pages_name

    pd.DataFrame({
        'Pages user has access to': InfoManager().project,
        'Approve': buttons
    })
    st.write(f"{InfoManager().users[a]} has access to {pages_name}")