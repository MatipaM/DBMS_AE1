class InfoManager():
    project  = ["Registeration", "login", "add book", "Home", "lib review", "manage_users", "payment", "request book","return book","users sales"]
    users = ["administrator", "student", "staff", "librarian"]

    librarian_pages = ["Registeration", "login", "add book", "Home", "lib review", "payment", "request book","return book","users sales"]
    administrator_pages = ["Registeration", "login", "add book", "Home", "lib review", "manage_users", "payment", "request book","return book","users sales"]
    staff_pages = ["Registeration", "login", "Home", "manage_users","manager", "payment", "request book","return book","users sales"]
    student_pages = ["Registeration", "login", "Home","manager", "payment", "request book","return book","users sales"] 

    user_pages_arrays = [administrator_pages,student_pages, staff_pages, librarian_pages]