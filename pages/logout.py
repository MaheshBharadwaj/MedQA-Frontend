import streamlit as st
from time import sleep

st.session_state["user"] = None
st.session_state["token"] = None

st.title("Medical QA Assistant - Logout")

st.info("You have been logged out successfully!")
sleep(1.3)
st.switch_page("pages/login.py")