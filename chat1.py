from dotenv import load_dotenv
load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai

# Configure API key for Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load the Gemini Pro model and start chat
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    """
    Function to get a response from the Gemini model.
    """
    # Send the question and get the response
    response = chat.send_message(question)
    return response

# Initialize Streamlit app
st.set_page_config(page_title="Q&A Demo")
st.header("KISAN Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Input field for user query in Kannada
input_text = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and input_text:
    try:
        # Get response from the model
        response = get_gemini_response(input_text)
        
        # Add user query and response to session state chat history
        st.session_state['chat_history'].append(("You", input_text))
        
        # Display response
        st.subheader("The Response is")
        for chunk in response:
            st.write(chunk.text)  # Display the response text
            st.session_state['chat_history'].append(("Bot", chunk.text))
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display the chat history
st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")

