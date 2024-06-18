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

st.write("Adminstrators")
df = pd.DataFrame(Project)
st.table(df)

st.write("Students")
df = pd.DataFrame(Project)
st.table(df)

st.write("staff")
df = pd.DataFrame(Project)
st.table(df)

st.write("Librarians")
df = pd.DataFrame(Project)
st.table(df)