import streamlit as st
from huggingface_hub import InferenceClient
from gtts import gTTS
from tempfile import NamedTemporaryFile
import os

# Initialize session state for storing conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Create a Streamlit app
st.title("AI Chat Companion")

# Set up the Hugging Face API client
api_key = "hf_ebB1LAKXMRCHbwWyZyCwLycoDBAxTqFxuR"  # Replace with your actual API key
client = InferenceClient(api_key=api_key)

# Define the model name
model_name = "meta-llama/Llama-3.2-11B-Vision-Instruct"

# Create a text input field
user_input = st.text_input("Enter your message:", "")

# Create a button to trigger the chatbot response
if st.button("Send"):
    if user_input.strip():  # Ensure input is not empty
        # Append user input to the conversation history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Prepare conversation messages as a single input
        conversation = "\n".join(
            f"{conv['role']}: {conv['content']}"
            for conv in st.session_state.conversation_history
        )

        try:
            # Get the chatbot response from Hugging Face
            response = client.query(
                model=model_name,
                inputs=conversation,
                max_length=500
            )

            # Extract the chatbot's response
            chatbot_response = response

            # Append the chatbot's response to the conversation history
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": chatbot_response
            })

            # Display the chatbot's response
            st.success("Chatbot Response:")
            st.write(chatbot_response)

            # Convert the response to speech using gTTS
            try:
                with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tts = gTTS(chatbot_response)
                    tts.save(tmp_file.name)
                    st.audio(tmp_file.name, format="audio/mp3")
                # Cleanup the temporary file after use
                os.remove(tmp_file.name)
            except Exception as audio_error:
                st.error(f"Audio generation failed: {audio_error}")

        except Exception as api_error:
            st.error(f"An error occurred with the API: {api_error}")
    else:
        st.warning("Please enter a message.")
