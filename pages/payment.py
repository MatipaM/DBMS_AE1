import streamlit as st
import time

#This is just a visual page, no functionality at all, just for end to end presentation

st.title("Payment Page")
st.write("Please enter your payment details below")
st.write("This is a dummy page, no payment will be processed.")

name = st.text_input("Name on Card")
card_number = st.text_input("Card Number")
expiry_date = st.date_input("Expiry Date")
cvv = st.text_input("CVV")

if st.button("Submit"):
    st.write("You will be redirected to the home page shortly.")
    
    store = st.empty()
    for i in range(3, 0, -1):
        store.write(f"Redirecting to the home page in {i} seconds...")
        time.sleep(1)

    st.switch_page("pages/payment_success.py")