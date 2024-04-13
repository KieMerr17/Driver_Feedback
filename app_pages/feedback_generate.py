import matplotlib.pyplot as plt
import streamlit as st
import random
import requests
import os
from openai import OpenAI
from env import OPENAI_API_KEY 

# example feedback
from feedback_examples.unit_1.unit_1_feedback import examples

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

def feedback_generate():
    st.write("#### To be used to quickly generate feedback for your driving sessions")
    
    # import drivers names and routes
    drivers = os.listdir("/workspace/Driver_Feedback/drivers")
    routes = os.listdir("/workspace/Driver_Feedback/routes")

    # Create a dropdown for the drivers and routes
    selected_driver = st.selectbox("Select a name", drivers)
    selected_route = st.selectbox("Select a route", routes)
    feedback_example = examples
    
    # Add a button to generate feedback
    if st.button("Generate Feedback"):
        prompt = f"Using the following as an example of good feedback: {feedback_example}, provide me feedback for {selected_driver} on {selected_route}?"
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                }
            ]
        }
        response = requests.post("https://api.openai.com/v1/chat/completions", json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            feedback_text = result['choices'][0]['message']['content'].strip()
            edited_feedback = st.text_area("Feedback", value=feedback_text, height=200)
            st.write("You can edit the feedback above.")
        else:
            st.error(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    feedback_generate()
