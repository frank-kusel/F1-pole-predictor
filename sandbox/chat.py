import streamlit as st
import numpy as np

# --- Chat input ---
prompt = st.chat_input("Say something")
if prompt:
    st.write(f"User has sent the following prompt: {prompt}")

# --- Chat messsage ---
# Insert charts, text, tables and more
with st.chat_message("user"):
    st.write("Hello 👋")
    st.line_chart(np.random.randn(30, 3))