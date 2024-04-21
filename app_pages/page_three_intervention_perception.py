import streamlit as st
import time

class SessionState:
    def __init__(self):
        self.timer_running = False
        self.start_time = None

session_state = SessionState()

def intervention_perception():
    st.title("Intervention Perception")
    st.write("Watch the video and click when you would carry out your intervention.")

    # Load the video and start time
    video_url = "https://drive.google.com/file/d/1MzXJThJxGZInmHmX6hYePeiZP4gn6SMb/view?usp=sharing"
    start_time = session_state.start_time if session_state.timer_running else 0
    st.video(video_url, format='video/mp4', start_time=start_time)

    button_slot = st.empty()  # Empty slot for the buttons

    if not session_state.timer_running:
        # Actions on clicking 'Play'
        if button_slot.button("Play"):
            session_state.timer_running = True
            session_state.start_time = time.time()
            button_slot.empty()  # Hide

    if session_state.timer_running:
        elapsed_time = time.time() - session_state.start_time

        # Actions on clicking 'Intervene'
        if button_slot.button("Intervene"):
            session_state.timer_running = False

            # Messages to display depending on intervention timing
            if elapsed_time < 5:
                st.write("Great that you intervened, have a think if this may have been a little early")
            elif 3.5 < elapsed_time < 5.5:
                st.write("Correct Intervention")
            else:
                st.write("Your Intervention was too late")

            session_state.start_time = None
            button_slot.empty()  # Hide

            # Actions on clicking 'Reset'
            if st.button("Reset"):
                session_state.timer_running = False
                session_state.start_time = None

if __name__ == "__main__":
    intervention_perception()

