import streamlit as st
import time

st.title("Your payment was successful! Thank you for your purchase!")
st.write("You will be redirected to the home page shortly.")

store = st.empty()
for i in range(3, 0, -1):
    store.write(f"Redirecting to the home page in {i} seconds...")
    time.sleep(1)

st.switch_page("pages/home.py")