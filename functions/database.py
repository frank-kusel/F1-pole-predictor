import sqlite3
from sqlite3 import Error
import streamlit as st


# Create a db connection
def create_connection(db_file):
    """Create a databse connection to a SQLite databse specified by a db_file
    :param: db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    
    except Error as e:
        print(e)
        
    return conn

# Create db tables
def create_table(conn, create_table_sql):
    """ create a table from the creat_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# Insert data
def register_user(conn, user_details):
    """
    Create a new user into the users table
    :param conn:
    :param user: username and password
    :return: user id
    """
    sql = ''' INSERT INTO users (username, password)
              VALUES(?,?)'''
    cur = conn.cursor()
    cur.execute(sql, user_details)
    conn.commit()
    return cur.lastrowid

# Function to save user guesses
def save_user_guesses(conn, user_guesses):
    """
    Insert user guesses into the user_guesses table
    :param conn:
    :param user_guesses: user_id, driver1, driver2, circuit
    :return:
    """
    sql = ''' INSERT INTO  user_guesses (user_id, driver1, driver2, circuit, submission_time)
                VALUES (?, ?, ?, ?, ?)'''
    cur = conn.cursor()
    cur.execute(sql, user_guesses)
    conn.commit()

# Function to check if username already exists
def is_username_taken(conn, username):
    """
    Check whether username already exists
    :param conn:
    :param username:
    :return: True or False
    """
    sql = ''' SELECT * FROM users WHERE username=?'''
    cur = conn.cursor()
    cur.execute(sql, username)
    return cur.fetchone() is not None

# Function to authenticate user
def authenticate_user(conn, login_details):
    """
    Authenticate user
    :param conn:
    :param login_details: username and password
    :return: True or False if user has logged in correctly
    """
    sql = ''' SELECT * FROM users WHERE username=? AND password=?'''
    cur = conn.cursor()
    cur.execute(sql, login_details)
    user_data = cur.fetchone()
    if user_data:
        user_id = int(user_data[0])
        return user_id  # Authentication successful
    else:
        return None  # Authentication failed


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