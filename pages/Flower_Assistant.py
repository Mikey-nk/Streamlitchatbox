import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")


genai.configure(api_key=api_key)
def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""
        You are a helpful, concise, accurate, and thoughtful AI assistant.
        Your primary role is to answer user questions comprehensively.
        Additionally, you are to provide detailed guides on various types of flowers, specifying their natural habitats and geographical distribution.
        The prompt is :{prompt}
        """,stream =True
    )
    return response

st.set_page_config(
    page_title = "Flower Assistant",
    page_icon="⚓"
)

st.title("Flower Assistant")

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "flowers_messages" not in st.session_state:
    st.session_state.flowers_messages = []
#display chat history

for msg in st.session_state.flowers_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#getting user input and feeding to model

if user_msg := st.chat_input("Ask me anything"):
    st.session_state.flowers_messages.append({"role":"user", "content":user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        full_response = ""
        try:
            streaming_response = stream_gemini_response(user_msg)
            for chunk in streaming_response:
                if chunk.text:
                    full_response += chunk.text
                    placeholder.markdown(full_response + " ")
            placeholder.markdown(full_response)
        except Exception as e:
            st.error(e)
    #adding the assistant's final response to the chat history
    st.session_state.flowers_messages.append({"role":"assistant", "content":full_response})
