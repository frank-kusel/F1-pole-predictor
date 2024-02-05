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

# TODO: Figure out how to access the session state from the main page in this page.
# TODO: Show table of picks once user has submitted their picks. 
# TODO: Show a summary of most picked drivers for the current race. 

st.title('Pole Picker')

# Connect to database
conn = sqlite3.connect('user_database.db')
c = conn.cursor()


# Function to fetch user guesses
c.execute("SELECT user_id, driver1, driver2, circuit FROM user_guesses")
guesses_data = c.fetchall()
df = pd.DataFrame(guesses_data, columns=['Name', 'Driver 1', 'Driver 2', 'Circuit'])
st.dataframe(df, use_container_width=True, hide_index=True)



st.bar_chart(np.random.randn(50, 3))

# --- Show scatterplot of driver picks ---
df = px.data.gapminder()
fig = px.scatter(
    df.query("year==2007"),
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    color="continent",
    hover_name="country",
    log_x=True,
    size_max=60,
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
