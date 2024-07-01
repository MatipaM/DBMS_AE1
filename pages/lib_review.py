import sqlite3
import pandas as pd
import streamlit as st
import pandas as pd
import os
from InfoManager import InfoManager

# Librarian Book Request Review
# 3 conditions: Returned all books AND paid outstanding bills, 

def display():
    st.header(f"Hello {st.session_state.first_name} {st.session_state.last_name}")
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #calc whether overdue instead of writing borrowed/returned date
    cursor.execute("SELECT pr.id, pr.email, pr.date_request, pr.title, pr.interest, pr.affiliation, b.author, b.publisher, b.year_purchased, b.year_published, b.description, b.secondary_title, b.version, b.quantity, b.available, b.rating, b.review, b.price, ob.email AS ob_email, ob.price AS ob_price FROM Pending_Request pr LEFT JOIN Books b ON pr.title = b.title LEFT JOIN Outstanding_Bills ob ON pr.email = ob.email;")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    st.write("### Add Books to Library")
    if st.button("Add Books"):
        st.switch_page("pages/add_book.py")

    st.write("### Pending Book Requests")

    if rows:
        df = pd.DataFrame(rows, columns=columns)
        df['Select'] = False
        df = st.data_editor(df, num_rows="dynamic")
    # else:
    #     st.write("No Book Requests.")

    approve_btn = ""
    disaprove_btn = ""


    try:
        df[df['Select'] ==True]
        approve_btn = st.button("Approve")
        disaprove_btn = st.button("Disapprove")
    except UnboundLocalError:
       approve_btn = st.write("There are no requests to approve")
       disaprove_btn = st.write("There are no requests to disapprove")

    # Approve or Disapprove Button
    if approve_btn:
        approved_requests = df[df['Select'] == True]

        for index, row in approved_requests.iterrows():
            cursor.execute(
                "INSERT INTO Book_records (id, borrowed_date, returned_date, email) VALUES (?, ?, NULL, ?)",
                (row['id'], row['date_request'], row['email'])
            )

            cursor.execute(
                "DELETE FROM Pending_Request WHERE title = ? AND email = ? AND date_request = ?",
                (row['title'], row['email'], row['date_request'])
            )
        conn.commit()
        df = df[df['Select'] == False]
        df.drop(columns=['Select'], inplace=True)
        st.write("You have approved the book request!")

    elif disaprove_btn:
        disapproved_requests = df[df['Select'] == True]
        reasons = []
        for index, row in disapproved_requests.iterrows():
            cursor.execute(
                "DELETE FROM Pending_Request WHERE title = ? AND email = ? AND date_request = ?",
                (row['title'], row['email'], row['date_request'])
            )
            conn.commit()
            cursor.execute("SELECT COUNT(*) FROM Book_records WHERE returned_date IS NULL")
            unreturned_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM Outstanding_Bills WHERE email = ?", (row['email'],))
            outstanding_count = cursor.fetchone()[0]
            
            reason = f"Request for {row['title']} by {row['email']} disapproved because: "
            if unreturned_count > 0:
                reason += "You have unreturned books. "
            if outstanding_count > 0:
                reason += "You have outstanding bills. "
            if not row['email'].endswith('@student.com'):
                reason += "Your email does not end with @student.com. "
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