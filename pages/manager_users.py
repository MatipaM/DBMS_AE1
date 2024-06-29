from flask import Flask, render_template, request
import streamlit as st
import pandas  as pd
st.title("Manage users")

st.write("Authenticate Adminstrators")
st.write("Authenticate Students")
st.write("Authenticate staff")
st.write("Autennticate Librarians")
st.title("Manage user Access")

Project  = ["Registeration", "login", "add book", "Home", "lib review", "manage users","manager", "payment", "request book","return book","users sales"]
column_headings = ["Pages user has access to", "Approve"]
buttons = []

# st.header("Adminstrators:")
# for i in Project:
#     new_select = st.checkbox(f"Select Administrators {i}");
#     buttons.append(new_select);

# df1 = pd.DataFrame({
#     'Pages user has access to': Project,
#     'Approve': buttons
# })

# st.header("Students:")
# buttons = []
# for i in Project:
#     new_select = st.checkbox(f"Select Students {i}");
#     buttons.append(new_select);

# df2 = pd.DataFrame({
#     'Pages user has access to': Project,
#     'Approve': buttons
# })

# st.header("staff:")
# buttons = []
# for i in Project:
#     new_select = st.checkbox(f"Select Staff {i}");
#     buttons.append(new_select);

# df3 = pd.DataFrame({
#     'Pages user has access to': Project,
#     'Approve': buttons
# })



positions = ["staff", "students", "administrator", "librarians"]
for a in range(4):
    st.header(positions[a])
    buttons=[]
    for b in Project:
        new_select = st.checkbox(f"{positions[a]}: approve access to {b} page");
        buttons.append(new_select);

    df4 = pd.DataFrame({
        'Pages user has access to': Project,
        'Approve': buttons
})