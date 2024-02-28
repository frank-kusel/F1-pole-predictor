import streamlit as st
import pandas as pd
import psycopg2

# Connect to PostgreSQL
@st.cache_resource
def connect_to_postgresql():
    conn = psycopg2.connect(
        dbname=st.secrets.postgresql.database,
        user=st.secrets.postgresql.username,
        password=st.secrets.postgresql.password,
        host=st.secrets.postgresql.host,
        port=st.secrets.postgresql.port
    )
    return conn

# # Function to execute query and fetch data
# @st.cache_data
# def fetch_data(_conn, query):
#     cur = _conn.cursor()
#     cur.execute(query)
#     rows = cur.fetchall()
#     df = pd.DataFrame(rows)
#     cur.close()  # Close cursor
#     return df

# Function to insert data
@st.cache_data
def insert_data(conn, query, params):
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()  # Close cursor


# Function to check if username already exists
@st.cache_data
def is_username_taken(_conn, username):
    query = 'SELECT * FROM users WHERE username = %s'
    with _conn.cursor() as cursor:
        cursor.execute(query, (username,))
        taken = cursor.fetchone()
        if taken:
            return True  # Taken
        else:
            return False  # Free

# Function to authenticate user
@st.cache_data
def authenticate_user(_conn, username, password):
    query = 'SELECT user_id FROM users WHERE username = %s AND password = %s LIMIT 1'
    with _conn.cursor() as cursor:
        cursor.execute(query, (username, password))
        user_data = cursor.fetchone()
        if user_data:
            user_id = user_data[0]
            return user_id  # Authentication successful
        else:
            return False  # Authentication failed



# Insert data: Register User
@st.cache_data
def register_user(_conn, username, password):
    query = "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;"
    with _conn.cursor() as cursor:
        cursor.execute(query, (username, password))
        user_id = cursor.fetchone()[0]
        _conn.commit()
    return user_id

# Function to save user guesses
@st.cache_data
def save_user_guesses(_conn, user_id, driver_1, driver_2, circuit_id, submission_time):
    query = '''
        INSERT INTO user_guesses (user_id, driver_1, driver_2, circuit_id, submission_time)
        VALUES (%s, %s, %s, %s, %s)
    '''
    with _conn.cursor() as cursor:
        cursor.execute(query, (user_id, driver_1, driver_2, circuit_id, submission_time))
        _conn.commit()
