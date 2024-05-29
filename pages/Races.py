'''
This page reveals various race statistics.  
'''

import streamlit as st
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import fastf1.plotting
import numpy as np
import streamlit as st
import fastf1
import plotly.graph_objects as go

def main():
    st.image("F_10_Pixel.png", use_column_width=True)
    navigation_menu()
    session = fastf1.get_session(2024, 8, "R")
    session.load()
    race_results()
    display_analysis(session)


def navigation_menu():
    with st.popover("Menu"):
        st.page_link("F1.py", label="Home", icon="🏠")
        st.page_link("pages/Driver Picks.py", label="Driver Picks", icon="🏇")
        st.page_link("pages/Stats.py", label="Stats", icon="🧐")
        st.page_link("pages/Welcome.py", label="Welcome", icon="😃")

@st.cache_data
def fetch_race_results(season):
    races = []
    offset = 0
    total_races = 30

    while len(races) < total_races:
        url = f"http://ergast.com/api/f1/{season}/results.json?limit=100&offset={offset}"
        response = requests.get(url)
        data = response.json()
        race_table = data["MRData"]["RaceTable"]

        for race in race_table.get("Races", []):
            for result in race.get("Results", []):
                race_data = {
                    "season": race["season"],
                    "round": race["round"],
                    "raceName": race["raceName"],
                    "circuitID": race["Circuit"]["circuitId"],
                    "country": race["Circuit"]["Location"]["country"],
                    "date": race["date"],
                    "driverID": result["Driver"]["driverId"],
                    "givenName": result["Driver"]["givenName"],
                    "familyName": result["Driver"]["familyName"],
                    "position": result["position"],
                    "constructorID": result["Constructor"]["constructorId"],
                    "grid": result["grid"],
                    "speed": result["FastestLap"]["AverageSpeed"]["speed"] if "speed" in result else None,
                    "time": result["Time"]["time"] if "Time" in result else None,
                }

                races.append(race_data)

        offset += 100
        total_races = int(data["MRData"]["total"])

    return races

def race_results():
    # if st.button("Home"):
    #     st.switch_page("F1.py")
    st.title("Races")

    st.info('View the season :red[**Schedule**] and  :red[**Results**] to compare final race positions vs starting grid positions.')

    st.subheader(':red[Schedule]')
    race_schedule = [
        {'raceName': 'Bahrain', 'date': '2024-03-02', 'circuitName': 'Bahrain International Circuit'},
        {'raceName': 'Saudi Arabian', 'date': '2024-03-09', 'circuitName': 'Jeddah Corniche Circuit'},
        {'raceName': 'Australian', 'date': '2024-03-24', 'circuitName': 'Albert Park Circuit'},
        {'raceName': 'Japanese', 'date': '2024-04-07', 'circuitName': 'Suzuka Circuit'},
        {'raceName': 'Chinese', 'date': '2024-04-21', 'circuitName': 'Shanghai International Circuit'},
        {'raceName': 'Miami', 'date': '2024-05-05', 'circuitName': 'Miami International Autodrome'},
        {'raceName': 'Emilia Romagna', 'date': '2024-05-19', 'circuitName': 'Autodromo Enzo e Dino Ferrari'},
        {'raceName': 'Monaco', 'date': '2024-05-26', 'circuitName': 'Circuit de Monaco'},
        {'raceName': 'Canadian', 'date': '2024-06-09', 'circuitName': 'Circuit Gilles Villeneuve'},
        {'raceName': 'Spanish', 'date': '2024-06-23', 'circuitName': 'Circuit de Barcelona-Catalunya'},
        {'raceName': 'Austrian', 'date': '2024-06-30', 'circuitName': 'Red Bull Ring'},
        {'raceName': 'British', 'date': '2024-07-07', 'circuitName': 'Silverstone Circuit'},
        {'raceName': 'Hungarian', 'date': '2024-07-21', 'circuitName': 'Hungaroring'},
        {'raceName': 'Belgian', 'date': '2024-07-28', 'circuitName': 'Circuit de Spa-Francorchamps'},
        {'raceName': 'Dutch', 'date': '2024-08-25', 'circuitName': 'Circuit Park Zandvoort'},
        {'raceName': 'Italian', 'date': '2024-09-01', 'circuitName': 'Autodromo Nazionale di Monza'},
        {'raceName': 'Azerbaijan', 'date': '2024-09-15', 'circuitName': 'Baku City Circuit'},
        {'raceName': 'Singapore', 'date': '2024-09-22', 'circuitName': 'Marina Bay Street Circuit'},
        {'raceName': 'United States', 'date': '2024-10-20', 'circuitName': 'Circuit of the Americas'},
        {'raceName': 'Mexico City', 'date': '2024-10-27', 'circuitName': 'Autódromo Hermanos Rodríguez'},
        {'raceName': 'São Paulo', 'date': '2024-11-03', 'circuitName': 'Autódromo José Carlos Pace'},
        {'raceName': 'Las Vegas', 'date': '2024-11-23', 'circuitName': 'Las Vegas Strip Street Circuit'},
        {'raceName': 'Qatar', 'date': '2024-12-01', 'circuitName': 'Losail International Circuit'},
        {'raceName': 'Abu Dhabi', 'date': '2024-12-08', 'circuitName': 'Yas Marina Circuit'}
        ]
    st.dataframe(
        race_schedule,
        column_order=("raceName", "date", "circuitName"),
        column_config={
            "raceName": "Grand Prix",
            "date": "Date",
            "circuitName": "Circuit Name",
        },
        hide_index=True,
        height=200,
        use_container_width=True,
    )

    st.subheader(":red[Results]")
    st.caption('*(Race results are fetched from somewhere else, and that somewhere else is sometimes not always there. Let the dough rise and come back later.)*')
    
    try:
        col1, col2 = st.columns(2)

        with col1:
            selected_season = st.selectbox("Select Season", list(range(2024, 2015, -1)))

        with col2:
            races = fetch_race_results(selected_season)
            df = pd.DataFrame(races)
            selected_race = st.selectbox("Select Race", df["raceName"].unique())

        filtered_df = df[df["raceName"] == selected_race]
        filtered_df = filtered_df.rename(
            columns={
                "position": "Position",
                "givenName": "Name",
                "familyName": "Surname",
                "time": "Time",
                "grid": "Grid",
            }
        )

        if not filtered_df.empty:
            st.dataframe(
                filtered_df[["Position", "Grid", "Name", "Surname", "Time"]].style.applymap(
                    color_position, subset=["Position", "Grid"]
                ),
                use_container_width=True,
                hide_index=True,
                height=738,
            )
        else:
            st.write("No data available for the selected season and race.")
    except Exception as e:
        st.error(f"Couldn't find somewhere else. Please try again later :) \n{e}")

def color_position(val):
    color = "red" if int(val) == 10 else "black"
    return f"background-color: {color}"

def display_analysis(session):
    st.header("Analysis")
    st.info("Analysis from the previous race")

    lap = session.laps.pick_fastest()
    pos = lap.get_pos_data()
    circuit_info = session.get_circuit_info()

    def rotate(xy, angle):
        rot_mat = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
        return np.matmul(xy, rot_mat)

    track = pos.loc[:, ("X", "Y")].to_numpy()
    track_angle = circuit_info.rotation / 180 * np.pi
    rotated_track = rotate(track, angle=track_angle)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=rotated_track[:, 0], y=rotated_track[:, 1], mode="lines", line=dict(color="red")))

    offset_vector = [600, 0]

    for _, corner in circuit_info.corners.iterrows():
        txt = f"{corner['Number']}{corner['Letter']}"
        offset_angle = corner["Angle"] / 180 * np.pi
        offset_x, offset_y = rotate(offset_vector, angle=offset_angle)
        text_x = corner["X"] + offset_x
        text_y = corner["Y"] + offset_y
        text_x, text_y = rotate([text_x, text_y], angle=track_angle)
        track_x, track_y = rotate([corner["X"], corner["Y"]], angle=track_angle)

        fig.add_trace(go.Scatter(x=[text_x], y=[text_y], mode="markers", marker=dict(color="grey", size=14)))
        fig.add_trace(go.Scatter(x=[track_x, text_x], y=[track_y, text_y], mode="lines", line=dict(color="grey")))
        fig.add_trace(go.Scatter(x=[text_x], y=[text_y], text=[txt], mode="text", textfont=dict(size=10, color="black")))

    fig.update_layout(
        dragmode=False,
        hovermode=False,
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        title=session.event["Location"],
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )

    with st.container(border=False):
        st.plotly_chart(fig, use_container_width=True)

    fastf1.plotting.setup_mpl(misc_mpl_mods=False)
    fig = go.Figure()

    for drv in session.drivers:
        drv_laps = session.laps.pick_driver(drv)
        abb = drv_laps["Driver"].iloc[0]
        color = fastf1.plotting.driver_color(abb)

        fig.add_trace(
            go.Scatter(
                x=drv_laps["LapNumber"],
                y=drv_laps["Position"],
                mode="lines",
                name=abb,
                line=dict(color=color),
            )
        )

    fig.update_layout(
        dragmode=False,
        yaxis_showgrid=False,
        xaxis_showline=False,
        yaxis_showline=False,
        yaxis_range=[0, 20],
        yaxis=dict(autorange="reversed", tickvals=list(range(1, 21))),
        height=433,
        xaxis=dict(showticklabels=False),
        legend=dict(
            orientation="v",
            yanchor="top",
            xanchor="left",
            x=1.01,
            y=0.985,
            bgcolor=st.get_option("theme.backgroundColor"),
            bordercolor=st.get_option("theme.backgroundColor"),
            font=dict(color="white"),
        ),
        xaxis_fixedrange=True,
        yaxis_fixedrange=True,
        margin=dict(l=0, r=0, t=30, b=0),
    )

    st.markdown("### Driver Position vs Laps")
    st.plotly_chart(fig, config={"displayModeBar": False, "scrollZoom": False}, use_container_width=True)


if __name__ == "__main__":
    main()
