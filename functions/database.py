import streamlit as st
import pandas as pd
import psycopg2
from datetime import date
from datetime import datetime

# Connect to PostgreSQL
def connect_to_postgresql():
    conn = psycopg2.connect(
        dbname=st.secrets.postgresql.database,
        user=st.secrets.postgresql.username,
        password=st.secrets.postgresql.password,
        host=st.secrets.postgresql.host,
        port=st.secrets.postgresql.port
    )
    return conn



def update_points_in_user_guesses(_conn):
    # Define the SQL query to select rows with empty points
    query = """
        SELECT guess_id, circuit_id, submission_time, driver_1, driver_2 
        FROM user_guesses 
        WHERE points IS NULL;
    """
    
    with _conn.cursor() as cursor:
        cursor.execute(query)
        guesses = cursor.fetchall()

        for guess in guesses:
            guess_id, circuit_id, submission_time, driver1, driver2 = guess

            # Extract the season from the submission_time (assuming submission_time is in the format 'YYYY-MM-DD hh:mm:ss')
            season = submission_time.year

            # Define the SQL query to retrieve driver positions
            query_positions = """
                SELECT position
                FROM race_results
                WHERE circuit_id = %s AND season = %s AND driver = %s
            """
            
            # Fetch driver positions from the database
            cursor.execute(query_positions, (circuit_id, season, driver1))
            driver1_position = cursor.fetchone()
            
            cursor.execute(query_positions, (circuit_id, season, driver2))
            driver2_position = cursor.fetchone()
            
            # Check if either driver position is None, and exit the function if so
            if driver1_position is None or driver2_position is None:
                # st.error("Error: Selected driver not found in race results")
                return

            # Process the positions
            driver1_position = driver1_position[0] if driver1_position else None
            driver2_position = driver2_position[0] if driver2_position else None
          
            # Calculate points based on the retrieved positions
            points_system = {
                "10": 25, "11": 18, "9": 15, "12": 12, "8": 10,
                "13": 8, "7": 6, "14": 4, "6": 2, "15": 1,
            }

            driver1_points = points_system.get(str(driver1_position), 0)
            driver2_points = points_system.get(str(driver2_position), 0) / 2

            # Determine the maximum points between driver1_points and driver2_points
            max_points = max(driver1_points, driver2_points)

            try:
                # Update the points in the user_guesses table
                cursor.execute("UPDATE user_guesses SET points = %s WHERE guess_id = %s", (max_points, guess_id))
            except Exception as e:
                print(f"Error updating points for guess_id {guess_id}: {e}")
    
    # Commit the changes
    _conn.commit()


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
def register_user(_conn, username, password):
    query = "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING user_id;"
    with _conn.cursor() as cursor:
        cursor.execute(query, (username, password))
        user_id = cursor.fetchone()[0]
        _conn.commit()
    return user_id

# Function to save user guesses

def save_user_guesses(_conn, user_id, driver_1, driver_2, circuit_id, submission_time):
    # Check if the user has already submitted a guess for the day
    today = date.today()
    formatted_today = today.strftime("%Y-%m-%d")
    query_check = '''
        SELECT COUNT(*) 
        FROM user_guesses 
        WHERE user_id = %s AND DATE(submission_time) = %s
    '''
    with _conn.cursor() as cursor:
        cursor.execute(query_check, (user_id, formatted_today))
        count = cursor.fetchone()[0]
        
    if count > 0:
        print("User has already submitted a guess for today.")
        
        return
    
    # If the user hasn't submitted a guess for the day, proceed to save the guess
    query_insert = '''
        INSERT INTO user_guesses (user_id, driver_1, driver_2, circuit_id, submission_time)
        VALUES (%s, %s, %s, %s, %s)
    '''
    with _conn.cursor() as cursor:
        cursor.execute(query_insert, (user_id, driver_1, driver_2, circuit_id, submission_time))
        _conn.commit()



def fetch_user_guesses(_conn):
    guesses_sql = '''   
                    SELECT
                        users.username,
                        user_guesses.driver_1,
                        user_guesses.driver_2,
                        user_guesses.points,
                        race_info.race_name,
                        TO_CHAR(race_info.date, 'MM-DD') AS race_date,
                        TO_CHAR(user_guesses.submission_time, 'YYYY') AS year
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
                       'race_name': 'Circuit',
                       'year': 'Year', 
                       'points': 'Points'
                       }, inplace=True)
    
    df['Race'] = df['Year'] + '-' + df['race_date'] + ' - ' + df['Circuit']
    df.drop(columns=['race_date'], inplace=True)
    # df.drop(columns=['submission_year', 'race_date'], inplace=True)
    return df


# driver picks
def fetch_driver_picks(_conn):
    driver_picks_sql = """ 
                    SELECT 
                        EXTRACT(YEAR FROM submission_time) AS year,
                        driver, 
                        COUNT(*) AS total_count
                    FROM (
                        SELECT driver_1 AS driver, submission_time FROM user_guesses WHERE EXTRACT(YEAR FROM submission_time) = 2024
                        UNION ALL
                        SELECT driver_2 AS driver, submission_time FROM user_guesses WHERE EXTRACT(YEAR FROM submission_time) = 2024
                    ) AS drivers
                    GROUP BY year, driver
                    ORDER BY year DESC, total_count DESC;

    """
    with _conn.cursor() as cursor:
        cursor.execute(driver_picks_sql)
        columns = [desc[0] for desc in cursor.description]
        driver_picks_db = cursor.fetchall()
    df = pd.DataFrame(driver_picks_db, columns=columns)
    return df

# Function to change user's password
def change_password(_conn, username, current_password, new_password):
    """
    Change user's password.
    
    Parameters:
    - _conn: psycopg2 connection object.
    - username: Username of the user whose password needs to be changed.
    - current_password: Current password of the user.
    - new_password: New password to set for the user.
    
    Returns:
    - True if password changed successfully, False otherwise.
    """
    # First, authenticate the user with the current password
    authenticated_user_id = authenticate_user(_conn, username, current_password)
    
    # If authentication fails, return False
    if not authenticated_user_id:
        return False
    
    # If authentication successful, update the password
    update_query = 'UPDATE users SET password = %s WHERE username = %s'
    with _conn.cursor() as cursor:
        try:
            cursor.execute(update_query, (new_password, username))
            _conn.commit()
            return True  # Password changed successfully
        except Exception as e:
            _conn.rollback()
            print(f"Error occurred while changing password: {e}")
            return False  # Password change failed


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


