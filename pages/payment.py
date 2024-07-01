import streamlit as st
import time
import os
from InfoManager import InfoManager

#This is just a visual page, no functionality at all, just for end to end presentation
def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
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


    InfoManager().get_instance().logout()

current_file_name = os.path.basename(__file__)

if hasattr(st.session_state, "first_name"):
    email = st.session_state.email
    first_name = st.session_state.first_name
    last_name = st.session_state.last_name
    affiliation = st.session_state.affiliation

    for idx,i in enumerate(InfoManager().get_instance().users):
        if st.session_state.affiliation == i:
            print("affiliation", st.session_state.affiliation)
            print(current_file_name, InfoManager().get_instance().getPages(idx))
            if current_file_name[:-3] in InfoManager().get_instance().getPages(idx):
                display()
            else:
                st.error(f"{first_name} {last_name}, {affiliation}'s are not authorised to view this page.")
                InfoManager().get_instance().logout()
else:
    InfoManager().get_instance().loginDefault()
    display()