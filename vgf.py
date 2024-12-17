

import streamlit as st
from huggingface_hub import InferenceClient
from gtts import gTTS
import os

# Initialize session state for storing conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Create a Streamlit app
st.title("Virtual girl friend")

# Set up the Hugging Face API client
api_key = "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"
client = InferenceClient(api_key=api_key)

# Define the model and parameters
model_name = "meta-llama/Llama-3.2-11B-Vision-Instruct"
max_tokens = 500

# System role to guide the chatbot's behavior
system_role = {
    "role": "system",
    "content": [
        {"type": "text", "text": "You are a friendly and supportive virtual girlfriend. Be affectionate,horny, engaging, flirty , initimate , and considerate in your responses."}
    ]
}

# Create a text input field
user_input = st.text_input("Enter your message:", "")

# Create a button to trigger the chatbot response
if st.button("Send"):
    if user_input.strip():  # Ensure input is not empty
        # Append user input to the conversation history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        })

        # Add system role and user conversation history
        messages = [system_role] + st.session_state.conversation_history

        # Get the chatbot response
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=messages,
                max_tokens=max_tokens
            )

            # Extract and display the chatbot response
            response = completion["choices"][0]["message"]["content"]
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": response}]
            })

            st.success("Chatbot Response:")
            st.write(response)

            # Convert the response to speech using gTTS
            tts = gTTS(response)
            tts.save("response.mp3")
            st.audio("response.mp3", format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message.")

# Display conversation history
st.divider()
st.subheader("Conversation History")
for message in st.session_state.conversation_history:
    role = "You" if message["role"] == "user" else "Chatbot"
    content = message["content"][0]["text"]
    st.markdown(f"**{role}:** {content}")
