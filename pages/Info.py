import streamlit as st

st.title("Info")

st.markdown('Keep an eye on this space for new features and updates...')


if st.button("Don't touch"):
    st.error("I can't believe you've done this!")

st.markdown('#### :green[Features]')
st.text('2024-03-03 : Points column added to view how many points your previous picks scored.')   
st.text('2024-03-02 : Races Page added.')

        

