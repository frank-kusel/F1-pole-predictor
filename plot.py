import matplotlib.pyplot as plt
import streamlit as st
import numpy as np

def plot_cumulative_points(cumulative_points):
     # Create a new figure
     fig, ax = plt.subplots()

     # Plot cumulative points for each user
     for user in cumulative_points.columns:
         final_points = cumulative_points[user].iloc[-1]
         if final_points >= 180:
             if cumulative_points[user].max() == cumulative_points.max().max():
                 ax.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=3, color='black')
             else:
                 ax.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=2)
         else:
             ax.plot(cumulative_points.index, cumulative_points[user], color='grey', alpha=0.3)

         # Annotate the plot with the name of the leader for each race
         prev_leader = None
         for i, race in enumerate(cumulative_points.index):
             leader = cumulative_points.loc[race].idxmax()
             leader_points = cumulative_points.loc[race, leader]
             if leader != prev_leader:
                 ax.text(i, leader_points + 15, leader, ha='center', va='bottom', fontsize=8, color='black', rotation=0, alpha=0.1)
                 ax.plot([i, i], [leader_points, leader_points + 10], color='black', linestyle='-', linewidth=0.1)
                 prev_leader = leader

     # Set labels and title
     ax.set_xlabel('Race')
     ax.set_ylabel('Leaderboard')
     ax.set_title('Cumulative Points by Race for Each User')
     num_races = 22
     ax.set_xticks(range(num_races))
     ax.set_ylim(0, cumulative_points.max().max()+50)
     plt.xticks(rotation=90)
     ax.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 8}, frameon=False)
     plt.tight_layout()
     ax.grid(color='gray', linestyle='--', linewidth=0.5)

     # Display the plot
     st.pyplot(fig)
