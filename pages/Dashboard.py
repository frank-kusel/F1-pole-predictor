import streamlit as st
import pandas as pd

# Initialize connection.
conn = st.connection("postgresql", type="sql")

'''
The page shows all Supabase tables. 
Only admin can see this page. 
'''

# users
st.subheader('Users')
users_df = conn.query('''SELECT * from users''', ttl=0.001)
st.dataframe(users_df, use_container_width=True, hide_index=True)

# user_guesses
st.subheader('User Guesses')
user_guesses_df = conn.query('''SELECT * FROM user_guesses ''')
st.dataframe(user_guesses_df, use_container_width=True, hide_index=True)

# race_info
st.subheader('Race Info')
race_info_df = conn.query('''SELECT * FROM race_info ''')
st.dataframe(race_info_df, use_container_width=True, hide_index=True)

# race_results
st.subheader('Race Results')
race_results_df = conn.query('''SELECT * FROM race_results ''')
st.dataframe(race_results_df, use_container_width=True, hide_index=True)

# scores
st.subheader('Scores')
scores_df = conn.query('''SELECT * FROM scores ''')
st.dataframe(scores_df, use_container_width=True, hide_index=True)