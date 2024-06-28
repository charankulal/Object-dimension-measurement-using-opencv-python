from tkinter import Image
import cv2
import streamlit as st
import numpy as np
import tempfile
from helpers import get_image_download_link


cap = cv2.VideoCapture(0)
# cap= cv2.VideoCapture('http://192.168.83.66:8080/video')
st.title("MEASUREMENT OF OBJECT DIMENSIONS - OPENCV")

frame_placeholder = st.empty()
col1, col2, col3, col4,  = st.columns(5)

with col2:
    start_button_pressed = st.button("Start")
with col3:
    stop_button_pressed = st.button("Stop")



while cap.isOpened() and start_button_pressed:
    ret, frame = cap.read()

    if not ret:
        st.write("The video capture has ended")
        break
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.flip(frame, 1)
    frame_placeholder.image(frame, channels="RGB")
    
    if cv2.waitKey(1) & 0xFF == ord("q") or stop_button_pressed:
        frame_placeholder = None

        break

cap.release()
cv2.destroyAllWindows()
