'''
For now this will show a bunch of tables for testing. 
Tables are queried from the db and shown as dataframes
'''
import functions.database as db
import streamlit as st
import pandas as pd


# Initialize connection.
conn = st.connection("postgresql", type="sql")

'''
This page shows a bunch of SQL queries and dataframes created from SQL queries to test out a few functions
'''

# users
st.subheader('Users')
users_df = conn.query('SELECT * from users')
st.dataframe(users_df, use_container_width=True, hide_index=True)

# user_guesses
st.subheader('User Guesses')
guess_id = 1
user_guesses_df = conn.query('''SELECT * 
                                FROM user_guesses 
                                WHERE guess_id = :guess_id''', params={"guess_id":"1"})

#  df = conn.query("select * from pet_owners where owner = :owner", ttl=3600, params={"owner":"barbara"}

st.dataframe(user_guesses_df, use_container_width=True, hide_index=True)


# driver picks
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
driver_picks_df = conn.query(driver_picks_sql)
st.subheader('Most Popular Driver')
st.dataframe(driver_picks_df, use_container_width=True, hide_index=True)
