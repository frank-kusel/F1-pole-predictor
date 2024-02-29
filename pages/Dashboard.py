import streamlit as st
import pandas as pd
import psycopg2

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

# Function to execute query and fetch data
def fetch_data(_conn, query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    df = pd.DataFrame(rows)
    cur.close()  # Close cursor
    return df

# Main code
conn = connect_to_postgresql()

# users
st.subheader('Users')
users_query = 'SELECT * FROM users;'
users_df = fetch_data(conn, users_query)
st.dataframe(users_df, use_container_width=True, hide_index=True)

# user_guesses
st.subheader('User Guesses')
user_guesses_query = 'SELECT * FROM user_guesses;'
user_guesses_df = fetch_data(conn, user_guesses_query)
st.dataframe(user_guesses_df, use_container_width=True, hide_index=True)

# race_info
st.subheader('Race Info')
race_info_query = 'SELECT * FROM race_info;'
race_info_df = fetch_data(conn, race_info_query)
st.dataframe(race_info_df, use_container_width=True, hide_index=True)

# race_results
st.subheader('Race Results')
race_results_query = 'SELECT * FROM race_results;'
race_results_df = fetch_data(conn, race_results_query)
st.dataframe(race_results_df, use_container_width=True, hide_index=True)

# scores
st.subheader('Scores')
scores_query = 'SELECT * FROM scores;'
scores_df = fetch_data(conn, scores_query)
st.dataframe(scores_df, use_container_width=True, hide_index=True)










# # users
# st.subheader('Users')
# users_df = conn.query('SELECT * FROM users;', ttl=None)
# st.dataframe(users_df, use_container_width=True, hide_index=True)

# # user_guesses
# st.subheader('User Guesses')
# user_guesses_df = conn.query('''SELECT * FROM user_guesses; ''')
# st.dataframe(user_guesses_df, use_container_width=True, hide_index=True)

# # race_info
# st.subheader('Race Info')
# race_info_df = conn.query('''SELECT * FROM race_info; ''')
# st.dataframe(race_info_df, use_container_width=True, hide_index=True)

# # race_results
# st.subheader('Race Results')
# race_results_df = conn.query('''SELECT * FROM race_results; ''')
# st.dataframe(race_results_df, use_container_width=True, hide_index=True)

# # scores
# st.subheader('Scores')
# scores_df = conn.query('''SELECT * FROM scores; ''')
# st.dataframe(scores_df, use_container_width=True, hide_index=True)