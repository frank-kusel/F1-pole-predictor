import sqlite3
import streamlit as st
from sqlalchemy import text
import pandas as pd

# Insert data
def register_user(conn, username, password):
    """
    Create a new user into the users table
    :param conn:
    :param user: username and password
    :return: user id
    """
    sql = text(''' INSERT INTO users (username, password)
              VALUES (:username, :password)''')
    with conn.session as s:
        s.execute(sql, params=dict(username=username, password=password))
        s.commit()
        

# Function to save user guesses
def save_user_guesses(conn, user_id, driver_1, driver_2, circuit_id, submission_time):
    """
    Insert user guesses into the user_guesses table
    :param conn:
    :param user_guesses: user_id, driver_1, driver_2, circuit
    :return:
    """
    sql = text('''   INSERT INTO user_guesses (user_id, driver_1, driver_2, circuit_id, submission_time)
                VALUES (:user_id, :driver_1, :driver_2, :circuit_id, :submission_time)''')
    with conn.session as s:
        s.execute(sql, params=dict(user_id=user_id, driver_1=driver_1, driver_2=driver_2, circuit_id=circuit_id, submission_time=submission_time))
        s.commit()


# Function to check if username already exists
def is_username_taken(conn, username):
    """
    Check whether username already exists
    :param conn:
    :param username:
    :return: True or False
    """
    sql = (''' SELECT * FROM users WHERE username = :username''')
    taken = conn.query(sql, params={"username": username})
    if not taken.empty:
        return True  # Taken
    else:
        return False  # Free

# Function to authenticate user
def authenticate_user(conn, username, password):
    """
    Authenticate user
    :param conn:
    :param username:
    :param password:
    :return: True or False if user has logged in correctly
    """
    sql = ('''   SELECT * 
                FROM 
                    users 
                WHERE 
                    username = :username AND password = :password''')
                    
    user_data = conn.query(sql, params={"username":username, "password":password})
    st.write(user_data)
    if not user_data.empty:
        user_id = pd.Dataframe(user_data)
        user_id = user_data.iloc[0, 0]

        return user_id  # Authentication successful
    else:
        return False  # Authentication failed


# Main function to handle user registration, login, and guess submission
def login(conn, database):
    """
    Register/authenticate a user and return user_id and TURE/FALSE for logged in status
    :param conn:
    :param database: username and password
    """
    
    # Registration or Login selection
    option = st.sidebar.radio("Select Option:", ("Register", "Login"), key="register_or_login")
    user_id = None
    
    if option == "Register":
        # Registration
        new_username = st.sidebar.text_input("Enter new username:")
        new_password = st.sidebar.text_input("Enter new password:", type="password")
        if st.sidebar.button("Register"):
            if is_username_taken(conn, (new_username,)):
                st.sidebar.warning("Username already taken. Please choose another one.")
            else:
                user_id = register_user(conn, (new_username, new_password))
                st.sidebar.success("Registration successful!")
        return user_id, False
    
    elif option == "Login":
        # Login
        username = st.sidebar.text_input("Username:")
        password = st.sidebar.text_input("Password:", type="password")
        logged_in = False
        if st.sidebar.button("Login"):
            user_id = authenticate_user(conn, (username, password))
            if not user_id == None:
                st.sidebar.success("Login successful!")
                st.sidebar.text(user_id)
                logged_in=True
 
            else:
                st.sidebar.error("Invalid username or password.")
                logged_in=False
                
        return user_id, logged_in


# TODO: this function is still WIP
def check_user_guess(conn, user_guess):
    """
    Check whether a user has already submitted a guess for a specific race.

    Args:
    - user_id: The ID of the user whose guess is being checked.
    - next_race_date: The date of the next race.

    Returns:
    - True if the user has not submitted a guess for the next race, False otherwise.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect('f1.db')

    # Query the database to check if the user has already submitted a guess for the next race
    query = f"SELECT * FROM user_guesses WHERE user_id = {user_id} AND date = '{next_race_date}'"
    df = pd.read_sql_query(query, conn)

    # Close the database connection
    conn.close()

    # If the DataFrame is empty, the user has not submitted a guess for the next race
    # Return True to allow the user to submit a new guess
    if df.empty:
        return True
    else:
        return False