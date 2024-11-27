Here is the refactored code with improvements:

```
import streamlit as st
from huggingface_hub import InferenceClient
from gtts import gTTS
import os

Initialize session state for storing conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

Create a Streamlit app
st.title("AI Chat Companion")

Set up the Hugging Face API client
api_key = "your_huggingface_api_key"  # Replace with your actual API key
client = InferenceClient(token=api_key)

Define the model and parameters
model_name = "meta-llama/Llama-3.2-11B-Vision-Instruct"
max_tokens = 500

System role to guide the chatbot's behavior
system_role = {
    "role": "system",
    "content": "You are a friendly assistant who helps users with their queries."
}

Create a text input field
user_input = st.text_input("Enter your message:", "")

Create a button to trigger the chatbot response
if st.button("Send"):
    if user_input.strip():  # Ensure input is not empty
        # Append user input to the conversation history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        # Prepare conversation messages
        messages = [system_role] + [{
            "role": conv["role"],
            "content": conv["content"]
        } for conv in st.session_state.conversation_history]

        try:
            # Get the chatbot response from Hugging Face
            response = client.text_generation(
                model=model_name,
                inputs={
                    "inputs": user_input,
                    "parameters": {"max_new_tokens": max_tokens}
                }
            )

            # Extract the chatbot's response
            chatbot_response = response.get("generated_text", "I'm sorry, I couldn't generate a response.")

            # Append the chatbot's response to the conversation history
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": chatbot_response
            })

            # Display the chatbot's response
            st.success("Chatbot Response:")
            st.write(chatbot_response)

            # Convert the response to speech using gTTS
            tts = gTTS(chatbot_response)
            audio_file = "response.mp3"
            tts.save(audio_file)
            st.audio(audio_file, format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message.")
```
