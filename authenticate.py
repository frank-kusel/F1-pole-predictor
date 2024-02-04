'''
This python script contains the logic required to authenticate a user. 
A user simply enters a name and password which is stored to the database. 
# TODO: I am not sure how databases work... so I don't know how to reset this or edit.. :|
'''

import streamlit as st
import sqlite3

# # Create table for user information
# c.execute('''CREATE TABLE IF NOT EXISTS users (
#              user_id INTEGER PRIMARY KEY AUTOINCREMENT,
#              username TEXT UNIQUE,
#              password TEXT)''')

# # Create table for user guesses
# c.execute('''CREATE TABLE IF NOT EXISTS user_guesses (
#              guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
#              user_id INTEGER,
#              driver1 TEXT,
#              driver2 TEXT,
#              FOREIGN KEY (user_id) REFERENCES users(user_id))''')

# Function to register new user
def register_user(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()

# Function to check if username already exists
def is_username_taken(username):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Function to authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

# Function to save user guesses
def save_user_guesses(user_id, driver1, driver2, circuit):
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()
    c.execute("INSERT INTO user_guesses (user_id, driver1, driver2, circuit) VALUES (?, ?, ?, ?)", (user_id, driver1, driver2, circuit))
    conn.commit()
    

# Main function to handle user registration, login, and guess submission
def login():
    conn = sqlite3.connect('user_database.db')
    c = conn.cursor()

    # Registration or Login selection
    option = st.sidebar.radio("Select Option:", ("Register", "Login"), key="register_or_login")

    if option == "Register":
        # Registration
        st.sidebar.header("Register")
        new_username = st.sidebar.text_input("Enter new username:")
        new_password = st.sidebar.text_input("Enter new password:", type="password")
        if st.sidebar.button("Register"):
            if is_username_taken(new_username):
                st.sidebar.warning("Username already taken. Please choose another one.")
            else:
                register_user(new_username, new_password)
                st.sidebar.success("Registration successful!")
        return None
    
    elif option == "Login":
        # Login
        st.sidebar.header("Login")
        username = st.sidebar.text_input("Username:")
        password = st.sidebar.text_input("Password:", type="password")
        if st.sidebar.button("Login"):
            if authenticate_user(username, password):
                st.sidebar.success("Login successful!")
 
            else:
                st.sidebar.error("Invalid username or password.")
        return username