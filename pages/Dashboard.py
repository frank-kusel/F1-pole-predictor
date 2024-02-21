'''
For now this will show a bunch of tables for testing. 
Tables are queried from the db and shown as dataframes
'''
import functions.database as db
import streamlit as st
import pandas as pd

database = r"f1.db"
conn = db.create_connection(database)


'''
This page shows a bunch of SQL queries and dataframes created from SQL queries to test out a few functions
'''




# --- SQLITE tables ---
st.header("SQL")
# users
st.subheader('Users')
users_df = pd.read_sql('SELECT * from users', conn)
st.dataframe(users_df, use_container_width=True, hide_index=True)

# user_guesses
st.subheader('User Guesses')
guess_id = 1
user_guesses_df = pd.read_sql('SELECT * from user_guesses WHERE guess_id=?', conn, params=(guess_id,))
st.dataframe(user_guesses_df, use_container_width=True, hide_index=True)

# --- SQL QUERY dataframes ---
st.header('QUERIES')

# driver picks
driver_picks_sql = """ SELECT driver, COUNT(*) AS total_count
            FROM (
                SELECT driver_1 AS driver FROM user_guesses
                UNION ALL
                SELECT driver_2 AS driver FROM user_guesses
            ) AS drivers
            GROUP BY driver
            ORDER BY total_count DESC;
"""
driver_picks_df = pd.read_sql(driver_picks_sql, conn)
st.subheader('Most Popular Driver')
st.dataframe(driver_picks_df, use_container_width=True, hide_index=True)
