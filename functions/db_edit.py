'''Run pieces of this code to edit the database. 
Warning: these changes are permanent'''

import streamlit as st
import sqlite3
import database as db
import pandas as pd


# Connect to database
database = r'f1.db'
conn = db.create_connection(database)

# --- Create tables ---
sql_create_users_table = """CREATE TABLE IF NOT EXISTS users ( 
                            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username text UNIQUE,
                            password text
                            ); """

sql_create_user_guesses_table = """ CREATE TABLE IF NOT EXISTS user_guesses (
                                    guess_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    user_id INTEGER,
                                    driver1 TEXT,
                                    driver2 TEXT,
                                    circuit TEXT,
                                    FOREIGN KEY (user_id) REFERENCES users (user_id)
                                    ); """

sql_create_race_results_table = """ CREATE TABLE IF NOT EXISTS race_results (
                                    race_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    circuit TEXT, 
                                    driver TEXT,
                                    position TEXT,
                                    time,
                                    stops,
                                    FOREIGN KEY (circuit) REFERENCES user_guesses (circuit) 
                                    ); """

# with conn:

    # # --- Delete items ---
    # conn.execute("DELETE FROM user_guesses WHERE Circuit = 'circuit'")
    # conn.execute("DELETE FROM user_guesses WHERE user_id IS NULL ")
    # conn.execute("DROP TABLE IF EXISTS race_results")
    
    # --- Create table ---
    # db.create_table(conn, sql_create_race_results_table)
    
    # --- Alter table ---
    # Alter table
    # conn.execute("ALTER TABLE race_results ADD COLUMN race_id INTEGER PRIMARY KEY;")
    # conn.execute("CREATE UNIQUE INDEX idx_race_id ON race_results (race_id);")
    
    # conn.commit()
    # conn.close()

# --- Read a dataframe to the database ---
# Define the file path
file_path = r'C:\Users\frank\F1-pole-predictor\data\2023_user_guesses.xlsx'

# # Read the Excel file into a DataFrame
# user_guesses_2023 = pd.read_excel(file_path, sheet_name='2023')
# user_names_2023 = pd.read_excel(file_path, sheet_name='2023')

# # Display the DataFrame
# print(user_guesses_2023)
# print(user_names_2023)

# # Assuming df is your DataFrame and database is your SQLite database file
# table_name_guesses = 'user_guesses'
# table_name_usernames = 'users'

# # Write DataFrame to SQLite table, append if table exists
# user_guesses_2023.to_sql(table_name_guesses, conn, if_exists='append', index=False)
# user_guesses_2023.to_sql(table_name_usernames, conn, if_exists='append', index=False)




# Read existing data from the SQLite table into a DataFrame
existing_data = pd.read_sql('SELECT * FROM users', conn)

# Load new data into a DataFrame (2023_user_guesses in this case)
new_data = pd.read_excel(file_path, sheet_name='users')

# Concatenate the existing data with the new data
combined_data = pd.concat([existing_data, new_data], ignore_index=True)

# Drop duplicates based on the primary key (assuming 'user_id' is the primary key)
combined_data_deduplicated = combined_data.drop_duplicates(subset='user_id')

# Append the deduplicated data to the SQLite table
combined_data_deduplicated.to_sql('users', conn, if_exists='replace', index=False)




# Close the connection
conn.close()