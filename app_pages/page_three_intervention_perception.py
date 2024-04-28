import streamlit as st
import base64
import os
import random
import time
from videos_and_timings import videos

# Begin timer when session video is loaded
class SessionState:
    def __init__(self):
        self.timer_running = False
        self.start_time = None

session_state = SessionState()


def intervention_perception():
    # Randomly select a video and format it to .mp4
    selected_video_dict = random.choice(videos)
    selected_video_key = list(selected_video_dict.keys())[0]
    intervention_start_time, intervention_end_time = selected_video_dict[selected_video_key]
    video_format = list(selected_video_dict.keys())[0] + ".mp4"

    # Display intervention window timings for selected video
    st.write("Intervention window start time: ", intervention_start_time)
    st.write("Intervention window end time: ", intervention_end_time)
    st.write(selected_video_key)

    # Directory of all videos
    media_dir = "/workspace/Driver_Feedback/media"

    if selected_video_key:
        # Load the video
        video_path = os.path.join(media_dir, video_format)
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
            if intervention_time < intervention_start_time:
                st.write("Great that you intervened, have a think if this may have been a little early")
            elif intervention_start_time < intervention_time < intervention_end_time:
                st.write("Correct Intervention")
            elif intervention_time > intervention_end_time:
                st.write("Your Intervention was too late")

    else:
        st.write("No video files found in the /media directory.")


if __name__ == "__main__":
    intervention_perception()