import streamlit as st
from constants import MAX_CHAT_HISTORY

def get_sidebar():
    with st.sidebar:
        st.title("MED QA")
        if st.button("Logout", use_container_width=True):
             st.switch_page("pages/logout.py")
        if st.button("New Chat", use_container_width=True):
                st.session_state["page_state"] = "new_chat"
                st.rerun()

        st.divider()
        
        st.subheader("Recent Chats")
        sample_chats = [
            {"id": f"chat_{i}", "timestamp": f"2024-03-{i}", "title": f"Chat {i}"} 
            for i in range(1, MAX_CHAT_HISTORY + 1)
        ]
        
        for chat in sample_chats:
            if st.button(
                f"{chat['title']} - {chat['timestamp']}", 
                key=chat['id'],
                use_container_width=True
            ):
                st.session_state["current_chat"] = chat['id']
                st.session_state["show_chat_form"] = False
                st.rerun()