import plotly.graph_objects as go
import streamlit as st

def plot_cumulative_points(cumulative_points):
    # Create a Plotly figure
    fig = go.Figure()

    # Plot cumulative points for each user
    for user in cumulative_points.columns:
        final_points = cumulative_points[user].iloc[-1]
        if final_points >= 180:
            if cumulative_points[user].max() == cumulative_points.max().max():
                fig.add_trace(go.Scatter(
                    x=cumulative_points.index,
                    y=cumulative_points[user],
                    mode='lines',
                    name=user,
                    line=dict(color='rgb(255, 51, 51)', width=3)
                ))
            else:
                fig.add_trace(go.Scatter(
                    x=cumulative_points.index,
                    y=cumulative_points[user],
                    mode='lines',
                    name=user,
                    line=dict(width=2),
                    opacity=0.3
                ))
        else:
            fig.add_trace(go.Scatter(
                x=cumulative_points.index,
                y=cumulative_points[user],
                mode='lines',
                name=user,
                line=dict(color='grey', width=1),
                opacity=0.3
            ))

    # Annotate the plot with the name of the leader for each race
    prev_leader = None
    for i, race in enumerate(cumulative_points.index):
        leader = cumulative_points.loc[race].idxmax()
        leader_points = cumulative_points.loc[race, leader]
        if leader != prev_leader:
            fig.add_annotation(
                x=i,
                y=leader_points,
                text=leader,
                showarrow=True,
                arrowcolor='grey',
                arrowside='end',
                arrowhead=1,
                font=dict(color='yellow'),
                opacity=0.5
            )
            prev_leader = leader

    # Update layout
    fig.update_layout(
        # title={'text': 'Leaderboard', 'x': 0.3, 'font': {'size': 24}},
        # xaxis=dict(title='Race'),
        # yaxis=dict(title='Points'),
        height=600,
        yaxis_gridwidth=False,
        yaxis_showgrid=False,  # Remove horizontal grid lines
        xaxis_tickangle=-90,
        xaxis_showline=False,
        yaxis_showline=False,
        xaxis_tickmode='array',
        xaxis_tickvals=list(range(22)),  # Assuming 22 races
        yaxis_range=[0, cumulative_points.max().max() + 50],
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=0.9,
            xanchor='center',
            x=0.5,
            bgcolor=st.get_option("theme.backgroundColor"),
            bordercolor=st.get_option("theme.backgroundColor"),
            font=dict(color='white')
        ),
        plot_bgcolor=st.get_option("theme.backgroundColor"),
        paper_bgcolor=st.get_option("theme.backgroundColor"),
        font=dict(color='white')
    )

    # Show the plot
    st.plotly_chart(fig, config ={'displayModeBar': False}, use_container_width=True)
