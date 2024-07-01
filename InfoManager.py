import streamlit as st

class InfoManager():
    project  = ["Registeration", "login", "add book", "Home", "lib review", "manage_users", "payment", "request book","return book","users sales"]
    users = ["administrator", "student", "staff", "librarian"]

    librarian_pages = ["registeration", "login", "add_book", "home", "lib_review", "payment", "request_book","return_book","user_sales"]
    administrator_pages = ["registeration", "login", "add add_book", "home", "lib_review", "manage_users", "payment", "request_book","return_book","user_sales"]
    staff_pages = ["registeration", "login", "home", "manage_users","manager", "payment", "request book","return book","users sales"]
    student_pages = ["registeration", "login", "home","manage_users", "payment", "request book","return book","users sales"] 

    user_pages_arrays = [administrator_pages,student_pages, staff_pages, librarian_pages]

    default_user={
        "first_name": "default_first_name",
        "last_name": "default_last_name",
        "email": "default@admistrator.com",
        "affiliation": "administrator"
    }

#change format of infomamnager nad manager users so that manager users resets infomamanger py 
    # def setPages(user_type, array_pages):
    #     user_pages_arrays[user_type] = array_pages;
