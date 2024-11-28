import streamlit as st
from constants import MAX_CHAT_HISTORY

def get_sidebar():
    chat_service = st.session_state["chat_service"]

    with st.sidebar:
        st.title("MED QA")
        if st.button("Logout", use_container_width=True):
             st.switch_page("pages/logout.py")
        if st.button("New Chat", use_container_width=True):
                st.session_state["page_state"] = "new_chat"
                st.rerun()

        st.divider()
        
        st.subheader("Recent Chats")
        user_chats = chat_service.get_user_chats(limit=MAX_CHAT_HISTORY)["chats"]

        for chat in user_chats:
            if st.button(
                f"{chat['title']}", 
                key=chat['chat_id'],
                use_container_width=True
            ):
                st.session_state["current_chat"] = chat['chat_id']
                st.session_state["show_chat_form"] = False
                st.rerun()