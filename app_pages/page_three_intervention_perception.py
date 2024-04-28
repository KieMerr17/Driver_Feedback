import streamlit as st
import base64
import os
import random
import time

# Video variables and intervention window times
videos = [
    {"video_1": (3.5, 4.5)},
    {"video_2": (4, 5)}
]

# Begin timer when session video is loaded
class SessionState:
    def __init__(self):
        self.timer_running = False
        self.start_time = None

session_state = SessionState()


def intervention_perception():
    # Randomly select a video
    selected_video_dict = random.choice(videos)
    selected_video_key = random.choice(list(selected_video_dict.keys())) + ".mp4"
    st.write(selected_video_key)

    # Directory of all videos
    media_dir = "/workspace/Driver_Feedback/media"


    if selected_video_key:
        # Load the video
        video_path = os.path.join(media_dir, selected_video_key)
        video_file = open(video_path, "rb").read()

        # Display the video
        video_id = "my_video"
        video_data = base64.b64encode(video_file).decode("utf-8")
        video_html = f"""
        <video id="{video_id}" controls autoplay width=640 height=360>
            <source src="data:video/mp4;base64,{video_data}" type="video/mp4">
            Your browser does not support the video tag.
        </video>
        """
        st.markdown(video_html, unsafe_allow_html=True)

        if not session_state.timer_running:
            session_state.start_time = time.time()
            session_state.timer_running = True

        elapsed_time = time.time() - session_state.start_time
        button_slot = st.button("Intervene")

        # Actions on clicking 'Intervene'
        if button_slot:
            intervention_time = elapsed_time - 3
            session_state.timer_running = False
            
            st.write(round(intervention_time, 2))

            # Messages to display depending on intervention timing
            if elapsed_time < 3.5:
                st.write("Great that you intervened, have a think if this may have been a little early")
            elif 3.5 < elapsed_time < 4.5:
                st.write("Correct Intervention")
            else:
                st.write("Your Intervention was too late")

    else:
        st.write("No video files found in the /media directory.")


if __name__ == "__main__":
    intervention_perception()