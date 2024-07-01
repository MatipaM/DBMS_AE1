import streamlit as st

class InfoManager():
    __instance = None   
    project  = ["registeration", "login", "add_book", "home", "lib_review", "manage_users", "payment", "request_book","return_book","user_sales"]

    librarian_pages = ["registeration", "login", "add_book", "home", "lib_review", "payment", "request_book","return_book","user_sales"]
    administrator_pages = ["registeration", "login", "add add_book", "home", "lib_review", "manage_users", "payment", "request_book","return_book","user_sales"]
    staff_pages = ["registeration", "login", "home", "manage_users","manager", "payment", "request book","return_book","users sales"]
    student_pages = ["registeration", "login", "home","manage_users", "payment", "request_book","return_book","users sales"] 
    
    users = ["administrator", "student", "staff", "librarian"]
    user_pages_arrays = [administrator_pages,student_pages, staff_pages, librarian_pages]

    default_user={
        "first_name": "default_first_name",
        "last_name": "default_last_name",
        "email": "default@admistrator.com",
        "affiliation": "administrator"
    }

# change format of infomamnager nad manager users so that manager users resets infomamanger py  
    @classmethod
    def setPages(cls,user_type, array_pages):
        cls.user_pages_arrays[user_type] = array_pages

    @classmethod
    def getPages(cls, user_type):
        return cls.user_pages_arrays[user_type]

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            print("Connecting to the database.")
            cls.__instance = cls()
        return cls.__instance
