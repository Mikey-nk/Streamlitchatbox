import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()
from numpy.matlib import empty

api_key = os.getenv("GEMINI_API_KEY")
#streaming responses to user

def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""
        You are a helpful assistant.
        You're role is to help the user with any of their questions.
        You are concise,accurate and thoughtful.
        You give the user step by step guides on anything that requires you to write a specific text.
        The prompt is :{prompt}
        """,stream =True
    )
    return response

st.set_page_config(
    page_title = "Writing Assistant",
    page_icon="⚓"
)

st.title("Writing Assistant")

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "writing_messages" not in st.session_state:
    st.session_state.writing_messages = []
#display chat history

for msg in st.session_state.writing_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#getting user input and feeding to model

if user_msg := st.chat_input("Ask me anything"):
    st.session_state.writing_messages.append({"role":"user", "content":user_msg})
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
    st.session_state.writing_messages.append({"role":"assistant", "content":full_response})
