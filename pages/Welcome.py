import streamlit as st

with st.popover("Menu"):
    st.page_link("F1.py", label="Home", icon="🏠")
    st.page_link("pages/Driver Picks.py", label="Driver Picks", icon="🏇")
    st.page_link("pages/Races.py", label="Races", icon="🏎️")
    st.page_link("pages/Stats.py", label="Stats", icon="🧐")

st.title("Welcome")

st.image('Tortoise.png', use_column_width=True)

with st.expander('Racing Rules'):
    # with st.expander("Racing Rules"):
    st.markdown('#### Racing Rules')
    st.markdown('_Welcome to the F1 - 10th Place Cup! Predict the 10th place driver and earn points._')
    st.markdown('Your first pick earns you the full points, and the second pick gets you half points. Whichever driver gives you the highest score will be used to calculate your points.')
    st.markdown('Driver picks must be submitted 1 hour before the race starts!')
    points_system = {
        "Position": ["10th", "11th", "9th", "12th", "8th", "13th", "7th", "14th", "6th", "15th"],
        "Points": [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]
    }
    # df_points_system = pd.DataFrame(points_system)
    st.dataframe(points_system, use_container_width=False, hide_index=True)

'''
Welcome to the F1 - 10th Place Cup, where the thrill of Formula 1 racing meets the excitement of prediction!

Our app brings you into the heart of the F1 action, allowing you to predict the 10th place driver in each race and earn points based on your predictions. It's not just about cheering for your favorite drivers; it's about testing your knowledge of the sport and seeing how your predictions stack up against others.

Whether you're a seasoned F1 fan or new to the world of motorsport, the F1 - 10th Place Cup offers you a chance to engage with the races in a whole new way. With every race, you have the opportunity to make your mark and climb the leaderboard.

To get started, simply register for an account or log in if you're already a member. Once logged in, you'll have access to the upcoming race schedule, where you can make your predictions for the 10th place driver. Will you go with a seasoned veteran or take a chance on an up-and-coming talent?

Don't worry if you're new to prediction games; our app makes it easy and fun to participate. And remember, it's not just about winning—it's about joining a community of passionate F1 fans who share your love for the sport.

So buckle up, get ready to experience the adrenaline of F1 racing like never before, and may the best predictor win!
'''

