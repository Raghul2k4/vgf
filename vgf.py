import streamlit as st
from huggingface_hub import InferenceClient
from gtts import gTTS

# Temporary session state for conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# App title
st.title("Virtual Girlfriend: Aroura")

# Hugging Face API client
api_key = "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"
client = InferenceClient(api_token=api_key)

# Model details
model_name = "meta-llama/Llama-3.2-11B-Vision-Instruct"
max_tokens = 500
max_input_tokens = 4096 - max_tokens  # Adjust based on token limit

# Define system role
system_role = {
    "role": "system",
    "content": [{"type": "text", "text": "You are a virtual girlfriend named Aroura. You are loving, affectionate, and engaging."}]
}

# Input field
user_input = st.text_input("Enter your message:", "")

# Clear history button
if st.button("Reset Conversation"):
    st.session_state.conversation_history = []
    st.success("Conversation history cleared.")

# Process user input
if st.button("Send"):
    if user_input.strip():
        # Add user input to conversation history
        st.session_state.conversation_history.append({
            "role": "user",
            "content": [{"type": "text", "text": user_input}]
        })

        # Combine system role and conversation history
        messages = [system_role] + st.session_state.conversation_history

        # Ensure history stays within token limits
        total_tokens = sum(len(msg["content"][0]["text"].split()) for msg in messages)
        if total_tokens > max_input_tokens:
            st.warning("Conversation too long, truncating earlier messages.")
            while total_tokens > max_input_tokens and st.session_state.conversation_history:
                removed_msg = st.session_state.conversation_history.pop(0)
                total_tokens -= len(removed_msg["content"][0]["text"].split())

        try:
            # Generate response
            completion = client.text_generation(
                model=model_name,
                inputs={"messages": messages},
                parameters={"max_new_tokens": max_tokens}
            )
            response = completion["generated_text"]

            # Add response to history
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": [{"type": "text", "text": response}]
            })

            # Display response
            st.success("Chatbot Response:")
            st.write(response)

            # Convert response to audio
            tts = gTTS(response)
            tts.save("response.mp3")
            st.audio("response.mp3", format="audio/mp3")

        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a message.")

# Display conversation history temporarily
st.divider()
st.subheader("Conversation History")
for message in st.session_state.conversation_history:
    role = "You" if message["role"] == "user" else "Chatbot"
    content = message["content"][0]["text"]
    st.markdown(f"**{role}:** {content}")
