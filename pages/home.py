import streamlit as st

st.title("Home Page")
st.write("Welcome to the Library Management System")

if 'disapproval_reasons' in st.session_state:
    reasons = st.session_state.disapproval_reasons
    for reason in reasons:
        st.write(reason)