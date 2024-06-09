import plotly.graph_objects as go
import streamlit as st
import pandas as pd
import plotly.express as px

# @st.cache_data
def plot_cumulative_points(cumulative_points):
    # Create a Plotly figure
    fig = go.Figure()

    # Get the index of the 10th position
    tenth_position = cumulative_points.iloc[-1].sort_values().index[9]

    # Sort the cumulative points by the final points
    sorted_cumulative_points = cumulative_points.iloc[-1].sort_values(ascending=False)

    # Get the top 20 names
    top_20_names = sorted_cumulative_points.index[:20]

    # Filter the cumulative points DataFrame to include only the top 20 names
    cumulative_points_top_20 = cumulative_points[top_20_names]

    # Plot cumulative points for each user (only the top 20 names)
    for user in cumulative_points_top_20.columns:
        final_points = cumulative_points_top_20[user].iloc[-1]
        if user == 0:
            fig.add_trace(go.Scatter(
                x=cumulative_points.index,
                y=cumulative_points_top_20[user],
                mode='lines+markers',
                name=user,
                line=dict(color='red', width=2)
            ))
        elif final_points >= 0.2*cumulative_points_top_20.max().max():
            if cumulative_points_top_20[user].max() == cumulative_points_top_20.max().max():
                fig.add_trace(go.Scatter(
                    x=cumulative_points.index,
                    y=cumulative_points_top_20[user],
                    mode='lines+markers',
                    name=user,
                    line=dict(color='green', width=3)
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=cumulative_points.index,
                    y=cumulative_points_top_20[user],
                    mode='lines',
                    name=user,
                    line=dict(width=1),
                    opacity=0.5
                ))
        else:
            fig.add_trace(go.Scatter(
                x=cumulative_points.index,
                y=cumulative_points_top_20[user],
                mode='lines',
                name=user,
                line=dict(color='grey', width=1),
                opacity=0.2
            ))


    # Initialize variables to track the previous leaders and their corresponding race names
    prev_leaders = None
    prev_race = None

    # Annotate the plot with the name of the leader(s) for each race
    for race in cumulative_points.index[1:]:
        leaders = cumulative_points.loc[race][cumulative_points.loc[race] == cumulative_points.loc[race].max()].index.tolist()
        
        # Check if the leaders are different from the previous race
        if leaders != prev_leaders:
            # Add annotation for the first unique race label
            if prev_race is not None:
                fig.add_annotation(
                    x=prev_race,
                    y=cumulative_points.loc[prev_race].max(),
                    text=', '.join(prev_leaders),
                    showarrow=True,
                    arrowcolor='grey',
                    arrowside='end',
                    arrowhead=6,
                    font=dict(color='grey'),
                    opacity=0.5,
                    textangle=-90,
                    xanchor='left',
                    ax=0,
                    ay=-30,                    
                )
            
            # Update previous leaders and race
            prev_leaders = leaders
            prev_race = race

    # Add annotation for the last unique race label
    if prev_race is not None:
        fig.add_annotation(
            x=prev_race,
            y=cumulative_points.loc[prev_race].max(),
            text=', '.join(prev_leaders),
            showarrow=True,
            arrowcolor='green',
            arrowside='end',
            arrowhead=6,
            font=dict(color='green'),
            opacity=1,
            textangle=-90,
            xanchor='left',
            ax=0,
            ay=-30,   
        )


    # Update layout
    fig.update_layout(
        # title={'text': 'Leaderboard', 'x': 0.3, 'font': {'size': 24}},
        # xaxis=dict(title='Race'),
        # yaxis=dict(title='Points'),
        dragmode=False,  # Disable panning
        # hovermode=False,  # Disable hover
        xaxis_fixedrange=True,  # Disable zoom on x-axis
        yaxis_fixedrange=True,  # Disable zoom on y-axis
        height=700,
        yaxis_gridwidth=False,
        yaxis_showgrid=False,  # Remove horizontal grid lines
        xaxis_tickangle=-90,
        xaxis_showline=False,
        yaxis_showline=False,
        xaxis_tickmode='array',
        xaxis_tickvals=list(range(22)),  # Assuming 22 races
        yaxis_range=[0, cumulative_points.max().max()+20],
        legend=dict(
            orientation='h',  # Horizontal orientation
            yanchor='bottom',
            y=1.2,
            xanchor='center',
            x=0.5,
            bgcolor=st.get_option("theme.backgroundColor"),
            bordercolor=st.get_option("theme.backgroundColor"),
            font=dict(color='white'),
            # itemsizing='constant'  # Ensure legend items have constant size
        ),
        plot_bgcolor=st.get_option("theme.backgroundColor"),
        paper_bgcolor=st.get_option("theme.backgroundColor"),
        font=dict(color='white'),
        yaxis=dict(
            showticklabels=False  # Remove y-axis tick labels
        )
    )

    # Show the plot
    st.plotly_chart(fig, config ={'displayModeBar': False, 'scrollZoom':False}, use_container_width=True)

@st.cache_data
def map_locations():
        # --- Plot a map ---
    data = [
    {"lon": 50.512, "lat": 26.031, "zoom": 15, "location": "Sakhir", "name": "Bahrain International Circuit", "id": "bh-2002"},
    {"lon": 39.104, "lat": 21.632, "zoom": 14, "location": "Jeddah", "name": "Jeddah Corniche Circuit", "id": "sa-2021"},
    {"lon": 144.970, "lat": -37.846, "zoom": 14, "location": "Melbourne", "name": "Albert Park Circuit", "id": "au-1953"},
    {"lon": 136.534, "lat": 34.844, "zoom": 15, "location": "Suzuka", "name": "Suzuka International Racing Course", "id": "jp-1962"},
    {"lon": 121.221, "lat": 31.340, "zoom": 14, "location": "Shanghai", "name": "Shanghai International Circuit", "id": "cn-2004"},
    {"lon": -80.239, "lat": 25.958, "zoom": 15, "location": "Miami", "name": "Miami International Autodrome", "id": "us-2022"},
    {"lon": 11.713, "lat": 44.341, "zoom": 15, "location": "Imola", "name": "Autodromo Enzo e Dino Ferrari", "id": "it-1953"},
    {"lon": 7.429, "lat": 43.737, "zoom": 15, "location": "Monaco", "name": "Circuit de Monaco", "id": "mc-1929"},
    {"lon": -73.525, "lat": 45.506, "zoom": 14, "location": "Montreal", "name": "Circuit Gilles-Villeneuve", "id": "ca-1978"},
    {"lon": 2.259, "lat": 41.569, "zoom": 14, "location": "Barcelona", "name": "Circuit de Barcelona-Catalunya", "id": "es-1991"},
    {"lon": 14.761, "lat": 47.223, "zoom": 15, "location": "Spielberg", "name": "Red Bull Ring", "id": "at-1969"},
    {"lon": -1.017, "lat": 52.072, "zoom": 14, "location": "Silverstone", "name": "Silverstone Circuit", "id": "gb-1948"},
    {"lon": 19.250, "lat": 47.583, "zoom": 14, "location": "Budapest", "name": "Hungaroring", "id": "hu-1986"},
    {"lon": 5.971, "lat": 50.436, "zoom": 13, "location": "Spa Francorchamps", "name": "Circuit de Spa-Francorchamps", "id": "be-1925"},
    {"lon": 4.541, "lat": 52.389, "zoom": 15, "location": "Zandvoort", "name": "Circuit Zandvoort", "id": "nl-1948"},
    {"lon": 9.290, "lat": 45.621, "zoom": 13, "location": "Monza", "name": "Autodromo Nazionale Monza", "id": "it-1922"},
    {"lon": 49.842, "lat": 40.369, "zoom": 14, "location": "Baku", "name": "Baku City Circuit", "id": "az-2016"},
    {"lon": 103.859, "lat": 1.291, "zoom": 15, "location": "Singapore", "name": "Marina Bay Street Circuit", "id": "sg-2008"},
    {"lon": -97.633, "lat": 30.135, "zoom": 15, "location": "Austin", "name": "Circuit of the Americas", "id": "us-2012"},
    {"lon": -99.091, "lat": 19.402, "zoom": 15, "location": "Mexico City", "name": "Autódromo Hermanos Rodríguez", "id": "mx-1962"},
    {"lon": -46.698, "lat": -23.702, "zoom": 15, "location": "Sao Paulo", "name": "Autódromo José Carlos Pace - Interlagos", "id": "br-1940"},
    {"lon": -115.168, "lat": 36.116, "zoom": 14, "location": "Las Vegas", "name": "Las Vegas Street Circuit", "id": "us-2023"},
    {"lon": 51.454, "lat": 25.49, "zoom": 15, "location": "Lusail", "name": "Losail International Circuit", "id": "qa-2004"},
    {"lon": 54.601, "lat": 24.471, "zoom": 14, "location": "Yas Marina", "name": "Yas Marina Circuit", "id": "ae-2009"}
    ]

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)

    # Create a scatter plot using Plotly
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", hover_name="name",
                            zoom=1, height=600, color_discrete_sequence=['red'])

    # Update map layout
    fig.update_layout(mapbox_style="carto-darkmatter")  # Dark map style
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

    # Hide latitude and longitude info when hovering
    fig.update_traces(hovertemplate="<b>%{hovertext}</b>")

    # Display the map in Streamlit
    st.markdown('### Race Locations')
    st.plotly_chart(fig, config ={'displayModeBar': False}, use_container_width=True)