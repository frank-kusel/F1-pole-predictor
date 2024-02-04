import streamlit as st
import pandas as pd
import numpy as np

# TODO: Show a map with the location of the next/current race
# TODO: Figure out whether an SQLConnection is required
# TODO: Create a connection to a data source or API
# TODO: Convert 2023 excel data to a datasource
# TODO: Streamlit Auth0: create user authentication or Authenticator
# TODO: Snowflake
# TODO: When the app starts, it should load the data required to popuplate driver names and circuit list
# https://discuss.streamlit.io/t/multi-page-app-with-session-state/3074
# https://discuss.streamlit.io/t/streamlit-authenticator-part-1-adding-an-authentication-component-to-your-app/34363

# --- random app ideas to implement later ---
# - text input: let user's submit comments?
# - additional bonus picks for:
#     - DNF driver of the day
#     - Fastest lap pick
#     - I changed my mind pick
# - Guess the fastest lap time with the st.time_input function - closest wins
# - Guess the finish time for the race - closest wins
# - Use file_uploader to allow user's to upload profile pics
# - Use colour_picker to allow user's to pick a colour
# - Create streamlit-lottie animations
# - Add tabs for some sort of race filtering.. not sure if this will work with filtering dataframes
# - Use the st.pydeck_chart to plot a 3Dish sort of map with race locations - interactive somehow??


actual_result = "Fernando Alonso"
st.info(f"10th Place: {actual_result}")

# --- Show a map ---
map_container = st.container(border=True)
df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])
map_container.map(df)
# st.map(df)