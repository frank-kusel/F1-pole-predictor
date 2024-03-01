'''
This page allows the user to select their drivers. 
Stats for drivers picked are revealed once the user's guess has been submitted. 
'''

import streamlit as st
import pandas as pd
import plotly.express as px
# import sqlite3
import plotly.graph_objects as go
import psycopg2
import functions.database as db

# TODO: Figure out how to access the session state from the main page in this page.
# TODO: Find a way to only show these results when race results are submitted

st.session_state

logged_in = st.session_state.get('logged_in')


# Initialize connection.
conn = psycopg2.connect(
    dbname=st.secrets.postgresql.database,
    user=st.secrets.postgresql.username,
    password=st.secrets.postgresql.password,
    host=st.secrets.postgresql.host,
    port=st.secrets.postgresql.port
)

if logged_in:
    
    # Fetch user guesses
    guesses_db = db.fetch_user_guesses(conn)
    df = guesses_db

    # Add a SelectBox to filter the DataFrame by circuit
    if st.button("Home"):
        st.switch_page("F1.py")
    st.title('Driver Picks')
    st.info("View driver picks for past races")
    
    selected_circuit = st.selectbox('Select Race', sorted(df['Race'].unique(), reverse=True))
    selected_circuit = selected_circuit.split("-")[3].strip()
    filtered_guesses_db = guesses_db[guesses_db['Circuit'] == selected_circuit]
    filtered_guesses_db.drop(columns=['Circuit'], inplace=True)
    filtered_guesses_db.drop(columns=['Race'], inplace=True)


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
        go.Bar(name='Driver 1', y=merged_counts['Driver'], x=merged_counts['Driver 1'], orientation='h', marker_color='red',text=merged_counts['Total'], textposition='auto'),
        go.Bar(name='Driver 2', y=merged_counts['Driver'], x=merged_counts['Driver 2'], orientation='h', marker_color='grey', text=merged_counts['Total'], textposition='auto')
    ])

    # Update layout
    fig.update_layout(barmode='stack',
                    dragmode=False,  # Disable panning
                    # hovermode=False,  # Disable hover
                    xaxis_fixedrange=True,  # Disable zoom on x-axis
                    yaxis_fixedrange=True,  # Disable zoom on y-axis
                    yaxis_title= None,
                    showlegend = False,
                    margin=dict(t=5),
                    xaxis=dict(showticklabels=False))  # Hide x-axis tick labels

    # Display the Plotly figure
    st.subheader('Race Picks')
    st.plotly_chart(fig, use_container_width=True, config ={'displayModeBar': False})
else:
    st.page_link("F1.py",label="Login to view guesses", icon="🔘", use_container_width=True)

# Fetch driver picks
driver_picks_df = db.fetch_driver_picks(conn)


st.subheader('Most Popular Driver')
# st.dataframe(driver_picks_df, use_container_width=True, hide_index=True)

# Create a stacked bar chart using Plotly
fig = go.Figure(data=[
    go.Bar(name='driver', y=driver_picks_df['driver'], x=driver_picks_df['total_count'], orientation='h', marker_color='red',text=driver_picks_df['total_count'], textposition='auto')
])

# Update layout
fig.update_layout( 
                    dragmode=False,  # Disable panning
                    # hovermode=False,  # Disable hover
                    xaxis_fixedrange=True,  # Disable zoom on x-axis
                    yaxis_fixedrange=True,  # Disable zoom on y-axis
                    yaxis_title= None,
                    showlegend = False,
                    height=800,
                    margin=dict(t=5),
                    xaxis=dict(showticklabels=False))  # Hide x-axis tick labels)

fig.update_yaxes(autorange="reversed")

# Display the Plotly figure
st.plotly_chart(fig, use_container_width=True, config ={'displayModeBar': False, 'editable': False})