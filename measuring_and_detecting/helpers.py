import streamlit as st
def toggle_start():
    st.session_state.start = True
    st.session_state.stop = False

def toggle_stop():
    st.session_state.stop = True
    st.session_state.start = False

def save_frame():
    st.session_state.save = True