import streamlit as st
import pandas as pd

# Initialize connection.
conn = st.connection("postgresql", type="sql")

'''
The page shows all Supabase tables. 
Only admin can see this page. 
'''



import psycopg2
import streamlit as st
import pandas as pd


# dialect = "postgresql"
# host = "aws-0-eu-west-2.pooler.supabase.com"
# port = "5432"
# database = "postgres"
# username = "postgres.xgubbnhhcfosnylqhlfk"
# password = "F7K11use!ZK"

# Connect to PostgreSQL
# conn = psycopg2.connect(
#     dbname="postgres",
#     user="postgres.xgubbnhhcfosnylqhlfk",
#     password="F7K11use!ZK",
#     host="aws-0-eu-west-2.pooler.supabase.com",
#     port="5432"
# )

# # Create a cursor object
# cur = conn.cursor()

# # Execute the query
# query = "SELECT * FROM users"
# cur.execute(query)

# # Fetch all rows from the result set
# rows = cur.fetchall()

# # Close the cursor and connection
# cur.close()
# conn.close()

# # Convert the result set to a pandas DataFrame
# users_df = pd.DataFrame(rows,)  # Specify column names as per your database schema

# # Display the DataFrame using Streamlit
# st.subheader('Users')
# st.dataframe(users_df)









# users
st.subheader('Users')
users_df = conn.query("SELECT * from users")
st.dataframe(users_df, use_container_width=True, hide_index=True)

# user_guesses
st.subheader('User Guesses')
user_guesses_df = conn.query('''SELECT * FROM user_guesses; ''')
st.dataframe(user_guesses_df, use_container_width=True, hide_index=True)

# race_info
st.subheader('Race Info')
race_info_df = conn.query('''SELECT * FROM race_info; ''')
st.dataframe(race_info_df, use_container_width=True, hide_index=True)

# race_results
st.subheader('Race Results')
race_results_df = conn.query('''SELECT * FROM race_results; ''')
st.dataframe(race_results_df, use_container_width=True, hide_index=True)

# scores
st.subheader('Scores')
scores_df = conn.query('''SELECT * FROM scores; ''')
st.dataframe(scores_df, use_container_width=True, hide_index=True)