import streamlit as st
from constants import MAX_CHAT_HISTORY

def get_sidebar():
    chat_service = st.session_state["chat_service"]

    with st.sidebar:
        st.title("MED QA")
        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Home 🏠", use_container_width=True):
                st.switch_page("main.py")
        with c2:
            if st.button("Logout 🔓", use_container_width=True):
                st.switch_page("pages/logout.py")
        if st.button("New Chat 💬", use_container_width=True):
            st.switch_page("pages/new_chat.py")

        st.divider()
        
        st.subheader("Recent Chats")
        user_chats = chat_service.get_user_chats(limit=MAX_CHAT_HISTORY)["chats"]

        for chat in user_chats:
            if st.button(
                f"{chat['title']}", 
                key=chat['chat_id'],
                use_container_width=True
            ):
                st.session_state["current_chat_id"] = chat['chat_id']
                st.switch_page("pages/chat.py")