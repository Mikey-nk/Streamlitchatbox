import streamlit as st
import google.generativeai as genai
import os

st.title('Medical Assistant')

from numpy.matlib import empty

api_key = os.getenv("GEMINI_API_KEY")
#streaming responses to user

def stream_gemini_response(prompt):
    model = genai.GenerativeModel(st.session_state.gemini_model)
    response = model.generate_content(
        f"""
        As a helpful assistant, your primary role is to answer user questions concisely, accurately, and thoughtfully.
        Specifically, you will address medical questions and provide step-by-step guides on achieving physical health
        The prompt is :{prompt}
        """,stream =True
    )
    return response

st.set_page_config(
    page_title = "Medical Assistant",
    page_icon="⚓"
)


if "gemini_model" not in st.session_state:
    st.session_state.gemini_model = "gemini-2.5-flash"

if "med_messages" not in st.session_state:
    st.session_state.med_messages = []
#display chat history

for msg in st.session_state.med_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

#getting user input and feeding to model

if user_msg := st.chat_input("Ask me anything"):
    st.session_state.med_messages.append({"role":"user", "content":user_msg})
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
    st.session_state.med_messages.append({"role":"assistant", "content":full_response})
