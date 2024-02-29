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


@st.cache_data
def fetch_user_guesses(_conn):
    guesses_sql = '''   
                    SELECT
                        users.username,
                        user_guesses.driver_1,
                        user_guesses.driver_2,
                        race_info.race_name,
                        TO_CHAR(race_info.date, 'MM-DD') AS race_date,
                        TO_CHAR(user_guesses.submission_time, 'YYYY') AS submission_year
                    FROM
                        user_guesses
                    JOIN
                        users ON user_guesses.user_id = users.user_id
                    JOIN
                        race_info ON user_guesses.circuit_id = race_info.circuit_id;
    '''
    with _conn.cursor() as cursor:
        cursor.execute(guesses_sql)
        columns = [desc[0] for desc in cursor.description]
        guesses_db = cursor.fetchall()
    df = pd.DataFrame(guesses_db, columns=columns)
    df.rename(columns={'username': 'User',
                       'driver_1': 'Driver 1',
                       'driver_2': 'Driver 2',
                       'race_name': 'Circuit'}, inplace=True)
    df['Race'] = df['submission_year'] + '-' + df['race_date'] + ' - ' + df['Circuit']
    df.drop(columns=['submission_year', 'race_date'], inplace=True)
    return df


# driver picks
@st.cache_data
def fetch_driver_picks(_conn):
    driver_picks_sql = """ 
                        SELECT 
                            driver, COUNT(*) AS total_count
                        FROM (
                            SELECT driver_1 AS driver FROM user_guesses
                            UNION ALL
                            SELECT driver_2 AS driver FROM user_guesses
                        ) AS drivers
                        GROUP BY driver
                        ORDER BY total_count DESC;
    """
    with _conn.cursor() as cursor:
        cursor.execute(driver_picks_sql)
        columns = [desc[0] for desc in cursor.description]
        driver_picks_db = cursor.fetchall()
    df = pd.DataFrame(driver_picks_db, columns=columns)
    return df
