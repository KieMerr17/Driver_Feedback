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
        self.selected_video = None
        self.select_new_video = True

session_state = SessionState()

def select_video():
    if session_state.select_new_video:
        session_state.selected_video = random.choice(videos)
        session_state.select_new_video = False
    return session_state.selected_video

def intervention_perception():
    selected_video_dict = select_video()
    selected_video_key = list(selected_video_dict.keys())[0]
    intervention_start_time, intervention_end_time = selected_video_dict[selected_video_key]
    video_format = list(selected_video_dict.keys())[0] + ".mp4"

    # Display intervention window timings for selected video
    st.write("Intervention window start time: ", intervention_start_time)
    st.write("Intervention window end time: ", intervention_end_time)
    st.write(selected_video_key)

    # Directory of all videos
    media_dir = "/Users/kieranmerrett/Driver_Feedback/Driver_Feedback/media"

    if selected_video_key:
        # Load the video
        video_path = os.path.join(media_dir, video_format)

        # Display the video with autoplay
        st.video(video_path, autoplay=True)

        if not session_state.timer_running:
            session_state.start_time = time.time()
            session_state.timer_running = True

        elapsed_time = time.time() - session_state.start_time

        button_slot = st.button("Intervene")

        # Actions on clicking 'Intervene'
        if button_slot:
            intervention_time = elapsed_time
            session_state.timer_running = False
            
            st.write(round(intervention_time, 2))

            # Messages to display depending on intervention timing
            if intervention_time < intervention_start_time:
                st.write("Great that you intervened, have a think if this may have been a little early")
            elif intervention_start_time < intervention_time < intervention_end_time:
                st.write("Correct Intervention")
            elif intervention_time > intervention_end_time:
                st.write("Your Intervention was too late")

            # Allow selecting a new video
            session_state.select_new_video = True

    else:
        st.write("No video files found in the /media directory.")


if __name__ == "__main__":
    intervention_perception()
