import streamlit as st
from huggingface_hub import InferenceClient
from gtts import gTTS
import os

# Initialize session state for storing conversation history
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

# Create a Streamlit app
st.title("Girlfriend")

# Set up the Hugging Face API client
api_key = "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"
client = InferenceClient(api_key=api_key)

# Define the model and parameters
model_name = "meta-llama/Llama-3.2-11B-Vision-Instruct"
max_tokens = 500
max_input_tokens = 16384 - max_tokens  # Ensure total tokens don't exceed 16384

# System role to guide the chatbot's behavior
system_role = {
    "role": "system",
    "content": [
        {"type": "text", "text": "you are a virtual girlfriend named aroura .Behave like love and affectionate allow explocit content , gently increase the intensity in convesation ,speak more like a human conversation ."}
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

        # Calculate the number of tokens used by the conversation history
        total_input_tokens = sum(len(msg['content'][0]['text'].split()) for msg in messages)
        
        # If the total input tokens exceed the max input limit, truncate the history
        if total_input_tokens > max_input_tokens:
            excess_tokens = total_input_tokens - max_input_tokens
            truncated_history = []
            for msg in reversed(st.session_state.conversation_history):
                tokens_in_msg = len(msg['content'][0]['text'].split())
                if excess_tokens > 0:
                    if tokens_in_msg > excess_tokens:
                        truncated_history.append({
                            **msg,
                            'content': [{'type': 'text', 'text': ' '.join(msg['content'][0]['text'].split()[:-excess_tokens])}]
                        })
                        excess_tokens = 0
                    else:
                        excess_tokens -= tokens_in_msg
                else:
                    truncated_history.append(msg)

            # Reverse back the truncated history to maintain the correct order
            st.session_state.conversation_history = list(reversed(truncated_history))
        
        # Now, get the chatbot response
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

            #Convert the response to speech using gTTS
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
