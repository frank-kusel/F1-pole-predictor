import sqlite3
import streamlit as st
import pandas as pd


# Streamlit app
st.title("F1 Prediction App - Database Viewer")

# Connect to SQLite database
conn = sqlite3.connect('app_database.db')
c = conn.cursor()

# Functions to interact with the database
def insert_user(username):
    c.execute("INSERT INTO Users (username) VALUES (?)", (username,))
    conn.commit()

def get_user_id(username):
    c.execute("SELECT user_id FROM Users WHERE username=?", (username,))
    row = c.fetchone()
    if row:
        return row[0]
    else:
        return None

# Input form to add new users
new_username = st.text_input("Enter your username:")
if st.button("Add User"):
    insert_user(new_username)
    st.success(f"User '{new_username}' added successfully!")


# Define function to fetch data from database tables
def fetch_data(table_name):
    c.execute(f"SELECT * FROM {table_name}")
    data = c.fetchall()
    columns = [description[0] for description in c.description]
    return pd.DataFrame(data, columns=columns)

# Select table to view
table_name = st.selectbox("Select Table", ["Users", "Races", "Guesses"])

# Fetch and display data
if table_name == "Users":
    st.write(fetch_data("Users"))
elif table_name == "Races":
    st.write(fetch_data("Races"))
elif table_name == "Guesses":
    st.write(fetch_data("Guesses"))

# Close database connection
conn.close()
