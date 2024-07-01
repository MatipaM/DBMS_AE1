import streamlit as st
import time
import os
from InfoManager import InfoManager

#This is just a visual page, no functionality at all, just for end to end presentation
def display():
    st.title("Payment Page")
    st.write("Please enter your payment details below")
    st.write("This is a dummy page, no payment will be processed.")

    name = st.text_input("Name on Card")
    card_number = st.text_input("Card Number")
    expiry_date = st.date_input("Expiry Date")
    cvv = st.text_input("CVV")

    if st.button("Submit"):
        st.write("Payment Successful! Thank you for your payment! You will be redirected to the home page shortly.")
        
        store = st.empty()
        for i in range(5, 0, -1):
            store.write(f"Redirecting to the home page in {i} seconds...")
            time.sleep(1)

        st.switch_page("pages/home.py")

    if st.button("logout"):
        if st.session_state.first_name is not "default_first_name":
            print("not default user")
            for key in st.session_state.keys():
                del st.session_state[key]
                InfoManager().get_instance().loginDefault()
                st.experimental_rerun()

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