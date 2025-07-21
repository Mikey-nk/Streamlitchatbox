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
        You are a helpful assistant.
        You're role is to help the user with any of their questions.
        You are concise,accurate and thoughtful.
        You give the user step by step guides on anything they enquire about.
        The prompt is :{prompt}
        """, stream=True
    )
    return response

st.set_page_config(
    page_title="General Assistant",
    page_icon="⚓"
)

st.title("General Chatbot")

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_msg := st.chat_input("Ask me anything"):
    st.session_state.messages.append({"role": "user", "content": user_msg})
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
    st.session_state.messages.append({"role": "assistant", "content": full_response})