import sqlite3
import pandas as pd
import streamlit as st
import pandas as pd

# Librarian Book Request Review
# 3 conditions: Returned all books AND paid outstanding bills, 

def display():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #calc whether overdue instead of writing borrowed/returned date
    cursor.execute("SELECT DISTINCT Book_records.borrowed_date, Book_records.returned_date, Books.rating, Books.review, Outstanding_Bills.title, Outstanding_Bills.affiliation, Outstanding_Bills.email, Outstanding_Bills.date_request FROM Outstanding_Bills LEFT JOIN Book_records ON Outstanding_Bills.email = Book_records.email LEFT JOIN Books ON Book_records.id = Books.id")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    st.write("### Pending Book Requests")

    if rows:
        df = pd.DataFrame(rows, columns=columns)
        df['Select'] = False
        df = st.data_editor(df, num_rows="dynamic")
    else:
        st.write("No Book Requests.")

    # Approve or Disapprove Button

    if st.button("Approve"):
        approved_requests = df[df['Select'] == True]

        for index, row in approved_requests.iterrows():
            cursor.execute(
                "INSERT INTO Book_Records (Title, Borrowed_Date, Email, Returned_Date, Rating, Review) VALUES (?, ?, ?, NULL, NULL, NULL)",
                (row['Title'], row['Request_Date'], row['Email'])
            )
            cursor.execute(
                "DELETE FROM Pending_Request WHERE Title = ? AND Email = ? AND Request_Date = ?",
                (row['Title'], row['Email'], row['Request_Date'])
            )
        conn.commit()
        conn.close()
        df = df[df['Select'] == False]
        df.drop(columns=['Select'], inplace=True)
        st.write("You have approved the book request!")

    elif st.button("Disapprove"):
        disapproved_requests = df[df['Select'] == True]
        reasons = []
        for index, row in disapproved_requests.iterrows():
            cursor.execute(
                "DELETE FROM Pending_Request WHERE Title = ? AND Email = ? AND Request_Date = ?",
                (row['Title'], row['Email'], row['Request_Date'])
            )
            conn.commit()
            cursor.execute("SELECT COUNT(*) FROM Book_Records WHERE Returned_Date IS NULL")
            unreturned_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Outstanding_Bills WHERE Email = ?", (row['Email'],))
            outstanding_count = cursor.fetchone()[0]
            
            reason = f"Request for {row['Title']} by {row['Email']} disapproved because: "
            if unreturned_count > 0:
                reason += "You have unreturned books. "
            if outstanding_count > 0:
                reason += "You have outstanding bills. "
            if not row['Email'].endswith('@student.com'):
                reason += "Your email does not end with @student.com. "
            # else:
            #     reason = "You are not a current student. If you are a current student, please contact the help@librarian.com"
            reasons.append(reason)
        conn.close()
        df = df[df['Select'] == False]
        df.drop(columns=['Select'], inplace=True)
        st.write("You have disapproved the book request!")

        #Students need to be notified
        st.session_state.disapproval_reasons = reasons

display()

# if "email" in st.session_state and 'first_name' in st.session_state and 'last_name' in st.session_state:
#     email = st.session_state.email
#     first_name = st.session_state.first_name
#     last_name = st.session_state.last_name
#     if "librarian" in email:
#         display()
#     else:
#         st.error(f"{first_name} {last_name}, you're {email} is not authorised to access this page.")
# else:
#     st.write("<a href='registration'>Please sign in</a>", unsafe_allow_html=True)