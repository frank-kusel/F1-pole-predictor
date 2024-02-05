# Assume we have the list of Formula 1 driver names
driver_names = [
    "Lewis Hamilton", "Max Verstappen", "Valtteri Bottas", "Lando Norris", "Sergio Perez",
    "Charles Leclerc", "Daniel Ricciardo", "Carlos Sainz", "Pierre Gasly", "Fernando Alonso",
    "Esteban Ocon", "Sebastian Vettel", "Lance Stroll", "Yuki Tsunoda", "Kimi Raikkonen",
    "Antonio Giovinazzi", "George Russell", "Mick Schumacher", "Nikita Mazepin", "Nicholas Latifi"
]

user_guess = "Fernando Alonso"

# Calculate points based on user's guess
if user_guess == driver_names[9]:
    points = 10
else:
    # Calculate bonus points based on proximity to the 10th position
    position_index = driver_names.index(user_guess)
    distance_from_10th = abs(10 - position_index)
    bonus_points = max(0, 5 - distance_from_10th)  # Assuming 5 bonus points for the closest guess
    points = bonus_points

# Store the user's points in the database (to be implemented)
# Display user's score and ranking on the leaderboard (to be implemented)
print(f'User score: {points}')
print('Hello user name! You scored %s points with %s' %(points, user_guess))

