import streamlit as st
import base64

# Function to add background image
def add_bg_from_local(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/jpg;base64,{encoded_string});
            background-size: cover;
        }}
        .header {{
            font-size: 50px; /* Font size */
            color: #4CAF50; /* Font color */
            font-weight: bold; /* Bold text */
            font-family: 'time New Roman', sans-serif; /* Font type */
        }}
        .input-container {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
        }}
        .input-label {{
            font-size: 16px; /* Font size */
            color: black; /* Font color */
            font-weight: bold; /* Bold text */
            font-family: 'Arial', sans-serif; /* Font type */
            margin-right: 10px; /* Space between label and input */
            width: 100px; /* Fixed width for labels */
        }}
        .input-field {{
            flex: 1;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Header with custom class for styling
st.markdown('<h1 class="header">Library Management System</h1>', unsafe_allow_html=True)

# Email input with label
st.markdown('<div class="input-container"><p class="input-label">Email:</p><input class="input-field" type="text" id="email" name="email"></div>', unsafe_allow_html=True)

# Password input with label
st.markdown('<div class="input-container"><p class="input-label">Password:</p><input class="input-field" type="password" id="password" name="password"></div>', unsafe_allow_html=True)

# Login button
st.button("Login", on_click=None, type="secondary", disabled=False, use_container_width=False)
