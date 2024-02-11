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


# TODO: Figure out how to access the session state from the main page in this page.
# TODO: Show table of picks once user has submitted their picks. 
# TODO: Show a summary of most picked drivers for the current race. 
# TODO: Find a way to only show these results when race results are submitted

st.title('Pole Picker')

# Connect to database
database = r'f1.db'
conn = sqlite3.connect(database)

c = conn.cursor()


# Function to fetch user guesses
c.execute("SELECT user_guesses.user_id, users.username, user_guesses.driver1, user_guesses.driver2, user_guesses.circuit FROM user_guesses JOIN users ON user_guesses.user_id = users.user_id")
guesses_data = c.fetchall()

df = pd.DataFrame(guesses_data, columns=['User ID', 'Name', 'Driver 1', 'Driver 2', 'Circuit'])


# Add a SelectBox to filter the DataFrame by circuit
selected_circuit = st.selectbox('Select Circuit', df['Circuit'].unique())

# Filter the DataFrame by selected circuit using .loc
filtered_df = df[df['Circuit'] == selected_circuit]

# Count occurrences of each driver as Driver 1 and Driver 2 separately
driver1_counts = filtered_df['Driver 1'].value_counts().reset_index()
driver2_counts = filtered_df['Driver 2'].value_counts().reset_index()

# Rename columns
driver1_counts.columns = ['Driver', 'Driver 1']
driver2_counts.columns = ['Driver', 'Driver 2']

# Merge counts for Driver 1 and Driver 2
merged_counts = pd.merge(driver1_counts, driver2_counts, on='Driver', how='outer').fillna(0)

# Convert counts to integers
merged_counts['Driver 1'] = merged_counts['Driver 1'].astype(int)
merged_counts['Driver 2'] = merged_counts['Driver 2'].astype(int)
merged_counts['Total'] = merged_counts['Driver 1'] + merged_counts['Driver 2']

st.dataframe(merged_counts, use_container_width=True, hide_index=True, )


# Combine the counts from Driver 1 and Driver 2
merged_counts['Total'] = merged_counts['Driver 1'] + merged_counts['Driver 2']

# Sort the DataFrame by Total Picks in descending order
merged_counts.sort_values(by='Total', ascending=True, inplace=True)


# Create a stacked bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(name='Driver 1', y=merged_counts['Driver'], x=merged_counts['Driver 1'], orientation='h', marker_color='green'),
    go.Bar(name='Driver 2', y=merged_counts['Driver'], x=merged_counts['Driver 2'], orientation='h', marker_color='orange')
])

# Update layout
fig.update_layout(barmode='stack',
                  xaxis_title='Number of Picks', 
                  yaxis_title= None,
                  showlegend = False,
                  title=f'Driver Picks for {selected_circuit}', legend=dict(title='Picks'))

# Display the Plotly figure
with st.container():
    st.plotly_chart(fig, use_container_width=True)

import matplotlib.pyplot as plt
import streamlit as st


st.markdown('raw dataframe - delete later')
st.dataframe(df, use_container_width=True, hide_index=True)

