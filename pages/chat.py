
import streamlit as st
from streamlit_mic_recorder import mic_recorder
from utils import speech_to_text
from sidebar import get_sidebar

get_sidebar()  

llm_service = st.session_state["llm_service"]
chat_service = st.session_state["chat_service"]
mode = st.session_state["llm_mode"]

st.title(st.session_state["chat_title"] or "Medical Consultation")
chat_container = st.container()
with chat_container:
    messages = chat_service.get_messages(st.session_state["current_chat_id"])["messages"]
    st.session_state["messages"] = [{"role": message["role"], "content": message["content"]} for message in messages]
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"].lower()):
            st.markdown(message["content"])

st.divider()

col1, col2 = st.columns([8, 1])

with col1:
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state["messages"].append({"role": "user", "content": user_input})
        chat_service.add_message(st.session_state["current_chat_id"], "user", user_input)
        try:
            response = llm_service.get_completion(st.session_state["messages"], mode=mode)["response"]
        except Exception as e:
            response = f"An error occurred! Please try again later"
            with st.expander("See error"):
                st.write(e)
        chat_service.add_message(st.session_state["current_chat_id"], "ai", response)
        st.session_state["messages"].append({
            "role": "ai",
            "content": response
        })
        st.rerun()

with col2:
    audio = mic_recorder(
        start_prompt="🎤",
        stop_prompt="⏹️",
        just_once=True,
        use_container_width=True
    )
    if audio:
        prompt = speech_to_text(audio)
        if prompt:
            st.session_state["messages"].append({
                "role": "user", "content": prompt
            })
            chat_service.add_message(st.session_state["current_chat_id"], "user", prompt)
            try:
                response = llm_service.get_completion(st.session_state["messages"], mode=mode)["response"]
            except Exception as e:
                response = f"An error occurred! Please try again later"
                with st.expander("See error"):
                    st.write(e)
            chat_service.add_message(st.session_state["current_chat_id"], "ai", response)
            st.session_state["messages"].append({
                "role": "ai",
                "content": response
            })
            st.rerun()