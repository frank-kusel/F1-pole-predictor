import numpy as np
import streamlit as st
import fastf1
import plotly.graph_objects as go

session = fastf1.get_session(2024, 2, 'R')
# session.load(telemetry=False, weather=False)
session.load()

lap = session.laps.pick_fastest()
pos = lap.get_pos_data()

circuit_info = session.get_circuit_info()

def rotate(xy, *, angle):
    rot_mat = np.array([[np.cos(angle), np.sin(angle)],
                        [-np.sin(angle), np.cos(angle)]])
    return np.matmul(xy, rot_mat)

# Get an array of shape [n, 2] where n is the number of points and the second
# axis is x and y.
track = pos.loc[:, ('X', 'Y')].to_numpy()

# Convert the rotation angle from degrees to radian.
track_angle = circuit_info.rotation / 180 * np.pi

# Rotate the track map.
rotated_track = rotate(track, angle=track_angle)

# Create a Plotly figure
fig = go.Figure()

# Plot the rotated track map
fig.add_trace(go.Scatter(x=rotated_track[:, 0], y=rotated_track[:, 1], mode='lines', line=dict(color='red')))

offset_vector = [600, 0]  # offset length is chosen arbitrarily to 'look good'

# Iterate over all corners.
for _, corner in circuit_info.corners.iterrows():
    # Create a string from corner number and letter
    txt = f"{corner['Number']}{corner['Letter']}"

    # Convert the angle from degrees to radian.
    offset_angle = corner['Angle'] / 180 * np.pi

    # Rotate the offset vector so that it points sideways from the track.
    offset_x, offset_y = rotate(offset_vector, angle=offset_angle)

    # Add the offset to the position of the corner
    text_x = corner['X'] + offset_x
    text_y = corner['Y'] + offset_y

    # Rotate the text position equivalently to the rest of the track map
    text_x, text_y = rotate([text_x, text_y], angle=track_angle)

    # Rotate the center of the corner equivalently to the rest of the track map
    track_x, track_y = rotate([corner['X'], corner['Y']], angle=track_angle)

    # Draw a circle next to the track.
    fig.add_trace(go.Scatter(x=[text_x], y=[text_y], mode='markers', marker=dict(color='grey', size=16)))

    # Draw a line from the track to this circle.
    fig.add_trace(go.Scatter(x=[track_x, text_x], y=[track_y, text_y], mode='lines', line=dict(color='grey')))

    # Finally, print the corner number inside the circle.
    fig.add_trace(go.Scatter(x=[text_x], y=[text_y], text=[txt], mode='text', textfont=dict(size=12, color='black')))

# Set the layout
fig.update_layout(
    dragmode=False,  # Disable panning
    hovermode=False,  # Disable hover
    xaxis_fixedrange=True,  # Disable zoom on x-axis
    yaxis_fixedrange=True,  # Disable zoom on y-axis
    title=session.event['Location'],
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    showlegend=False,
    # aspectratio=dict(x=1, y=1),
    margin=dict(l=0, r=0, t=40, b=0)  # Adjust margins to fit the title
)

# Show the plot
with st.container(border=False):
    st.plotly_chart(fig, use_container_width=True)




# Driver Laptimes Scatterplot
# ==============================

# Plot a driver's lap times in a race, with color coding for the compounds.




import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import fastf1.plotting

# Set up matplotlib for Fast F1
fastf1.plotting.setup_mpl(misc_mpl_mods=False)

# Create a Plotly figure
fig = go.Figure()

# For each driver, plot their position over the number of laps
for drv in session.drivers:
    drv_laps = session.laps.pick_driver(drv)

    abb = drv_laps['Driver'].iloc[0]
    color = fastf1.plotting.driver_color(abb)

    fig.add_trace(go.Scatter(
        x=drv_laps['LapNumber'],
        y=drv_laps['Position'],
        mode='lines',
        name=abb,
        line=dict(color=color)
    ))

# Finalize the plot
fig.update_layout(
    dragmode=False,  # Disable panning
    yaxis_showgrid=False,
    xaxis_showline=False,
    yaxis_showline=False,
    yaxis_range=[0,20],
    yaxis=dict(autorange='reversed', tickvals=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]),
    height=433,
    xaxis=dict(
    showticklabels=False,  # Remove x-axis tick labels
    ),
    legend=dict(
        orientation='v',
        yanchor='top',
        xanchor='left',
        x=1.01,
        y=0.985,
        bgcolor=st.get_option("theme.backgroundColor"),
        bordercolor=st.get_option("theme.backgroundColor"),
        font=dict(color='white')
    ),
    xaxis_fixedrange=True,  # Disable zoom on x-axis
    yaxis_fixedrange=True,  # Disable zoom on y-axis
    margin=dict(l=0, r=0, t=30, b=0),  # Adjust margin to accommodate legend
)

# Show the plot using Streamlit
st.plotly_chart(fig, config ={'displayModeBar': False, 'scrollZoom':False}, use_container_width=True)



