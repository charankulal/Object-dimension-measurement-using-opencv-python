import cv2
import streamlit as st
import numpy as np

def main():
    # Initialize session state variables
    if 'start' not in st.session_state:
        st.session_state.start = False
    if 'stop' not in st.session_state:
        st.session_state.stop = False
    if 'save' not in st.session_state:
        st.session_state.save = False

    st.title("MEASUREMENT OF OBJECT DIMENSIONS - OPENCV")

    frame_placeholder = st.empty()
    col1, col2, col3, col4, col5 = st.columns(5)

    with col2:
        st.button("Start", on_click=toggle_start)
    with col3:
        st.button("Stop", on_click=toggle_stop)
    with col4:
        st.button("Save", on_click=save_frame)

    if st.session_state.start and not st.session_state.stop:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.write("The video capture has ended")
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)
            frame_placeholder.image(frame, channels="RGB")

            if st.session_state.save:
                frame=cv2.cvtColor(frame,cv2.COLOR_BGRA2RGB)
                cv2.imwrite("frame.png", frame)
                st.session_state.save = False  # Reset save flag after saving

            if st.session_state.stop:
                frame_placeholder.empty()
                break

        cap.release()
        cv2.destroyAllWindows()

def toggle_start():
    st.session_state.start = True
    st.session_state.stop = False

def toggle_stop():
    st.session_state.stop = True
    st.session_state.start = False

def save_frame():
    st.session_state.save = True

if __name__ == "__main__":
    main()
