import sqlite3
import pandas as pd
import streamlit as st
import pandas as pd

# Librarian Book Request Review
# 3 conditions: Returned all books, paid outstanding bills, and current student
# Use hello@gmail.com to test!!!!

conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM Pending_Request")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

st.write("### Pending Book Requests")

if rows:
    df = pd.DataFrame(rows, columns=columns)
    df['Select'] = False
    df = st.data_editor(df, num_rows="dynamic")
else:
    st.write("No Book Requests.")


# Criteria 1 (Returned all books)

st.write("### Checklist 1: Outstanding Books")
cursor.execute("SELECT br.Title, br.Borrowed_Date, br.Returned_Date, br.Email AS Borrower_Email, br.Rating, br.Review, pr.Affiliation, pr.Interest, pr.Email AS Requester_Email, pr.Request_Date FROM Book_Records br JOIN Pending_Request pr ON br.Email = pr.Email WHERE (br.Borrowed_Date IS NOT NULL AND br.Returned_Date IS NOT NULL) OR (br.Borrowed_Date IS NOT NULL AND br.Returned_Date IS NULL)")
row2 = cursor.fetchall()
column2 = [description[0] for description in cursor.description]

if row2:
    df2 = pd.DataFrame(row2, columns=column2)
    df2 = st.data_editor(df2, num_rows="dynamic")
else:
    st.write("No outstanding books.")

# Criteria 2 (Paid outstanding bills)

st.write("### Checklist 2: Outstanding Bills")
cursor.execute("SELECT ob.Email AS Outstanding_Bill_Email, ob.Amount FROM Outstanding_Bills ob JOIN Pending_Request pr ON ob.Email = pr.Email WHERE ob.Amount IS NOT NULL")
row3 = cursor.fetchall()
column3 = [description[0] for description in cursor.description]

if row3:
    df3 = pd.DataFrame(row3, columns=column3)
    df3 = st.data_editor(df3, num_rows="dynamic")
else:
    st.write("No outstanding bills.")

# Criteria 3 (Current Student)

st.write("### Checklist 3: Current Student")

cursor.execute("SELECT Email, Affiliation FROM Pending_Request")
row4 = cursor.fetchall()
column4 = [description[0] for description in cursor.description]


if row4:
    df4 = pd.DataFrame(row4, columns=column4)
    df4 = st.data_editor(df4, num_rows="dynamic")
else:
    st.write("No current students.")

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
    st.write("Approved!")

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
        else:
            reason = "You are not a current student. If you are a current student, please contact the help@librarian.com"
        
        reasons.append(reason)
    conn.close()
    df = df[df['Select'] == False]
    df.drop(columns=['Select'], inplace=True)
    st.write("Disapproved!")

    #Students need to be notified
    st.session_state.disapproval_reasons = reasons



