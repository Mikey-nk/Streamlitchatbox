import streamlit as st
import google.generativeai as genai
import os

# Load API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("Google API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# streaming responses to user
def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""
        As a helpful, concise, accurate, and thoughtful AI assistant,
        your primary role is to provide comprehensive information
        and guidance on automotive subjects.
        This includes, but is not limited to, different types of vehicles,
        their historical development, specific models,
        and the various components that make up an automobile.
        The prompt is :{prompt}
        """, stream=True
    )
    return response

st.set_page_config(
    page_title="Cars Assistant",
    page_icon="⚓"
)

st.title("Cars Assistant")

if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "cars_messages" not in st.session_state:
    st.session_state.cars_messages = []

# display chat history
for msg in st.session_state.cars_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# getting user input and feeding to model
if user_msg := st.chat_input("Ask me anything"):
    st.session_state.cars_messages.append({"role": "user", "content": user_msg})
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
    # adding the assistant's final response to the chat history
    st.session_state.cars_messages.append({"role": "assistant", "content": full_response})