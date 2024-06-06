import matplotlib.pyplot as plt
import streamlit as st
import random
import requests
import os

# Importing the API key from env.py
from env import OPENAI_API_KEY

# information required to generate feedback
from form_info import routes, examples

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}"
}

# Connect to Chat GPT to create feedback using selected fields
def generate_feedback(selected_driver, type_of_feedback, selected_route, positive_feedback, negative_feedback):

    # Choose which example to use depending on route selected
    if selected_route == "Unit 1 - High Standard Driving":
        example_data = examples["Unit 1"]
    elif selected_route == "Unit 2 - CRT Millbrook":
        example_data = examples["Unit 2"]
    else:
        example_data = examples["Open-Road Testing"]

    # Message to be sent to Chat GPT
    prompt = f"Using the following as an example of good feedback: {example_data}, provide me with brand new {type_of_feedback} feedback for {selected_driver} on {selected_route}. Include {positive_feedback}, but also areas for improvement in {negative_feedback} give simple bullet points afterwords using {negative_feedback} on areas of improvement. Make sure everything reads as one complete feedback report, make sure selections are not enclosed in brackets or quotation marks"

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

        # Print out just the message provided in Chat GPT result
        feedback_text = result['choices'][0]['message']['content'].strip()
        return feedback_text
    else:
        # Error handling
        st.error(f"Error: {response.status_code} - {response.text}")
        return None

# Information to be displayed on the page
def feedback_page():
    st.title("Feedback Generator")
    st.write("#### To be used to quickly generate feedback for your driving sessions")

    # Create the drop down menus
    selected_driver = st.text_input("Enter the driver's name:")
    type_of_feedback = st.selectbox("Select which type of feedback required", ["Positive", "Constructive", "Negative"])
    selected_route = st.multiselect("Select all routes required", routes)
    positive_feedback = st.text_input("What did they do well? (Separate points by commas)")
    negative_feedback = st.text_input("What do they need to improve? (Separate points by commas)")

    
    # Add a button to generate feedback
    if st.button("Generate Feedback"):
        feedback_text = generate_feedback(selected_driver, type_of_feedback, selected_route, positive_feedback, negative_feedback)
        if feedback_text is not None:
            edited_feedback = st.text_area("Feedback", value=feedback_text, height=200)
            st.write("You can edit the feedback above.")

if __name__ == "__main__":
    feedback_page()
