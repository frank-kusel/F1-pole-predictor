''''
Stats for the discerning user
'''
import streamlit as st

with st.expander("Menu"):
    st.page_link("F1.py", label="Home", icon="🏠")
    st.page_link("pages/Driver Picks.py", label="Driver Picks", icon="🏇")
    st.page_link("pages/Stats.py", label="Stats", icon="🧐")
    st.page_link("pages/Welcome.py", label="Welcome", icon="😃")

st.header("Stats")

st.info('Stats for the discerning user 🧐')

st.text('Coming soon...')

# st.text_input("Suggestion: ")
# suggestion_button = st.button('Submit suggestion', key='suggestions')
# if suggestion_button:
#     st.text("I don't do anything yet...")

st.subheader('Races')
st.markdown(f" :red[Predicatable-prix] - race with the most winners")
st.markdown(f" :red[Fast-and-confuscious] - races with no winners")
st.markdown(f"- :green[Saudi Arabian Grand Prix]")

st.subheader('Players')
st.markdown(f" :red[Maximum-verstappen] - player with longest streak in 1st place")
st.markdown(f" :red[Yuki-know-if-yuki-know] - player with the longest streak in 10th place")
st.markdown(f" :red[Minimum-verstappen] - players with longest losing streak")
st.markdown(f" :red[No-gasly] - player who consistently picks the slowest driver")
st.markdown(f" :red[Formula-none] - player with the most missed submissions")
st.markdown(f" :red[Zeroes-to-heroes] - players who managed to win after losing")
st.markdown(f" :red[Heroes-to-zeroes] - plauers who managed to lose after winning")
st.markdown(f" :red[Sheep-shifter] - player who most often picks grid 10 as their first pick")
st.markdown(f" :red[Backmarker-whisperer] - player who consistently predicts the last driver")
st.markdown(f" :red[Gambling-gunther] - player who picks drivers starting furthest from 10th starting position")
st.markdown(f" :red[Sargent-safety] - player with the most consistent early submissions")
st.markdown(f" :red[The-haas-and-the-tortoise] - player with the slowest submissions")




# List of races where no one had any idea what they were doing
# Zeroes-to-heroes (players who managed to win after scoring 0 the previous round)
# Heroes-to-zeroes
# Fast finger: 
# Most winners for a race
# '''