'''
This page allows the user to select their drivers. 
Stats for drivers picked are revealed once the user's guess has been submitted. 
'''

import streamlit as st
import pandas as pd
import calendar
import numpy as np
import plotly.express as px
import sqlite3
import plotly.graph_objects as go
from st_supabase_connection import SupabaseConnection
import functions.database as db
from supabase import create_client, Client

# TODO: Figure out how to access the session state from the main page in this page.
# TODO: Find a way to only show these results when race results are submitted

# Initialize connection.
conn = st.connection("postgresql", type="sql")

# Perform query.
guesses_sql = '''   
            SELECT 
                users.username,
                user_guesses.driver_1, 
                user_guesses.driver_2, 
                race_info.race_name 
            FROM 
                user_guesses 
            JOIN 
                users ON user_guesses.user_id = users.user_id
            JOIN
                race_info ON user_guesses.circuit_id = race_info.circuit_id
'''

guesses_db = conn.query(guesses_sql, ttl=None)
guesses_db.rename(columns={'username': 'User',
                           'driver_1': 'Driver 1',
                           'driver_2': 'Driver 2',
                           'race_name': 'Circuit'},inplace=True)

df = guesses_db

# Add a SelectBox to filter the DataFrame by circuit
st.subheader('Driver Picks')
selected_circuit = st.selectbox('', df['Circuit'].unique())
filtered_guesses_db = guesses_db[guesses_db['Circuit'] == selected_circuit]
filtered_guesses_db.drop(columns=['Circuit'], inplace=True)


st.dataframe(filtered_guesses_db, hide_index=True, use_container_width=True)

# Filter the DataFrame by selected circuit using .loc
filtered_df = df[df['Circuit'] == selected_circuit]

# Count occurrences of each driver as Driver 1 and Driver 2 separately
driver_1_counts = filtered_df['Driver 1'].value_counts().reset_index()
driver_2_counts = filtered_df['Driver 2'].value_counts().reset_index()

# Rename columns
driver_1_counts.columns = ['Driver', 'Driver 1']
driver_2_counts.columns = ['Driver', 'Driver 2']

# Merge counts for Driver 1 and Driver 2
merged_counts = pd.merge(driver_1_counts, driver_2_counts, on='Driver', how='outer').fillna(0)

# Convert counts to integers
merged_counts['Driver 1'] = merged_counts['Driver 1'].astype(int)
merged_counts['Driver 2'] = merged_counts['Driver 2'].astype(int)
merged_counts['Total'] = merged_counts['Driver 1'] + merged_counts['Driver 2']

# st.dataframe(merged_counts, use_container_width=True, hide_index=True, )


# Combine the counts from Driver 1 and Driver 2
merged_counts['Total'] = merged_counts['Driver 1'] + merged_counts['Driver 2']

# Sort the DataFrame by Total Picks in descending order
merged_counts.sort_values(by='Total', ascending=True, inplace=True)


# Create a stacked bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(name='Driver 1', y=merged_counts['Driver'], x=merged_counts['Driver 1'], orientation='h', marker_color='red'),
    go.Bar(name='Driver 2', y=merged_counts['Driver'], x=merged_counts['Driver 2'], orientation='h', marker_color='grey')
])

# Update layout
fig.update_layout(barmode='stack',
                  xaxis_title='Number of Picks', 
                  yaxis_title= None,
                  showlegend = False,
                  margin=dict(t=5))

# Display the Plotly figure
st.subheader('Race Picks')
st.plotly_chart(fig, use_container_width=True, config ={'displayModeBar': False})



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
# st.dataframe(driver_picks_df, use_container_width=True, hide_index=True)

# Create a stacked bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(name='driver', y=driver_picks_df['driver'], x=driver_picks_df['total_count'], orientation='h', marker_color='red',text=driver_picks_df['total_count'], textposition='auto')
])

# Update layout
fig.update_layout( 
                  yaxis_title= None,
                  showlegend = False,
                  height=800,
                  margin=dict(t=5))

fig.update_yaxes(autorange="reversed")

# Display the Plotly figure
st.plotly_chart(fig, use_container_width=True, config ={'displayModeBar': False, 'editable': False})