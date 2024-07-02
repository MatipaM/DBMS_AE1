import streamlit as st

class InfoManager():
    __instance = None   
    project  = ["registration", "login", "add_book", "home", "lib_review", "manage_users", "payment", "request_book","return_book","user_sales"]

    librarian_pages = ["registration", "login", "add_book", "home", "lib_review", "payment", "request_book","return_book","user_sales"]
    administrator_pages = ["registration", "login", "add_book", "home", "lib_review", "manage_users", "payment", "request_book","return_book","user_sales"]
    staff_pages = ["registration", "login", "home", "manage_users","manager", "payment", "request book","return_book","user_sales"]
    student_pages = ["registration", "login", "home","manage_users", "payment", "request_book","return_book","user_sales"] 
    
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

    @classmethod
    def loginDefault(cls):
        st.session_state.first_name = cls.default_user["first_name"]
        st.session_state.last_name = cls.default_user["last_name"]
        st.session_state.email = cls.default_user["email"]
        st.session_state.affiliation = cls.default_user["affiliation"]

    @staticmethod
    def logout():
        if st.session_state.first_name != "default_first_name":
            if st.button("logout"):
                print("not default user")
                for key in st.session_state.keys():
                    del st.session_state[key]
                    InfoManager().get_instance().loginDefault()
                    logout_btn = st.button("login")
                    st.experimental_rerun()
        elif st.button("login"):
            st.switch_page("pages/2_login.py")
                    
