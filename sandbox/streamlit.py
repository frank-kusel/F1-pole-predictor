# import sandbox.streamlit as st
# import pandas as pd
# import matplotlib.pyplot as plt


# def plot_cumulative_points():
#     # Load data
#     df = pd.read_excel('F1_data.xlsm', sheet_name='Results', index_col=0)
#     print(df)
#     df = df.T
#     cumulative_points = df.cumsum()

#     # Create a new figure
#     fig, ax = plt.subplots()

#     # Plot cumulative points for each user
#     for user in cumulative_points.columns:
#         final_points = cumulative_points[user].iloc[-1]  # Get the final points for the user
#         if final_points >= 180:  # Grey out users with less than 150 points
#             if cumulative_points[user].max() == cumulative_points.max().max():  # Check if this user has the highest points
#                 ax.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=3, color='black')  # Make line bold
#             else:
#                 ax.plot(cumulative_points.index, cumulative_points[user], label=user, linewidth=2)
#         else:
#             ax.plot(cumulative_points.index, cumulative_points[user], color='grey', alpha=0.3)

#         # Initialize previous leader
#         prev_leader = None
#         leader_count = {user: 1 for user in cumulative_points.columns}

#         # Annotate the plot with the name of the leader for each race
#         for i, race in enumerate(cumulative_points.index):
#             leader = cumulative_points.loc[race].idxmax()  # Get the user with the highest points for this race
#             leader_points = cumulative_points.loc[race, leader]  # Get the points of the leader for this race

#             # Check if the leader has changed
#             if leader != prev_leader:
#                 # Position the label higher above the plotting point
#                 ax.text(i, leader_points + 15, leader, ha='center', va='bottom', fontsize=8, color='black', rotation=0, alpha=0.1)

#                 # Add a leader line pointing down to the plotting point
#                 ax.plot([i, i], [leader_points, leader_points + 10], color='black', linestyle='-', linewidth=0.1)

#                 # Update the previous leader
#                 prev_leader = leader

#     exit()

#     # Set labels and title
#     ax.set_xlabel('Race')
#     ax.set_ylabel('Cumulative Points')
#     ax.set_title('Cumulative Points by Race for Each User')
#     num_races = 22
#     ax.set_xticks(range(num_races))
#     ax.set_ylim(0, cumulative_points.max().max()+50)
#     plt.xticks(rotation=90)
#     ax.legend(loc='upper left', bbox_to_anchor=(1, 1), prop={'size': 8}, frameon=False)  # Adjust font size as needed
#     plt.tight_layout()
#     ax.grid(color='gray', linestyle='--', linewidth=0.5)

#     # Display the plot
#     st.pyplot(fig)

# def main():
#     st.title("F1 Pole Predictor")
#     st.markdown("Welcome to the F1 Prediction Game! Predict the 10th place driver and earn points.")

#     # Get user's guess
#     user_guess = st.text_input("Enter your guess for the 10th place driver:", "")

#     # Display the actual result (for demo purposes)
#     actual_result = "Fernando Alonso"
#     st.info(f"Actual 10th place driver: {actual_result}")

#     # Calculate points based on the user's guess and display the result
#     points = 10
#     st.success(f"You scored {points} points for your guess!")

#     # Plot cumulative points
#     st.header("Cumulative Points")
#     plot_cumulative_points()

# # Run the app
# if __name__ == "__main__":
#     main()
