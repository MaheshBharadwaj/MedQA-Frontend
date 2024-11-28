import streamlit as st
from streamlit_mic_recorder import mic_recorder
import openai

from constants import MAX_CHAT_HISTORY, OPENAI_API_KEY
from sidebar import get_sidebar
from utils import *
from datetime import datetime

openai.api_key = OPENAI_API_KEY
openai_client = openai.Client()

st.set_page_config(page_title="Medical QA Assistant")

get_sidebar()

# Initialize session state
if "openai_client" not in st.session_state:
    st.session_state["openai_client"] = openai_client
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "page_state" not in st.session_state:
    print("Setting welcome state")
    st.session_state["page_state"] = "welcome"  # Can be: welcome, new_chat, conversation
if "chat_title" not in st.session_state:
    st.session_state["chat_title"] = None


def reset_chat_state():
    st.session_state["messages"] = []
    st.session_state["chat_title"] = None

def show_welcome_page():
    st.title("Welcome to Medical QA Assistant")
    st.write("""
    👋 Welcome to your medical assistant! I'm here to help answer your medical questions 
    and provide reliable information based on your health history and concerns.
    
    To get started:
    - Click 'New Chat' in the sidebar to begin a new conversation
    - Or select a recent chat to continue a previous discussion
    """)
    
    if st.session_state["messages"]:
        st.divider()
        st.subheader("Your Latest Conversation")
        for message in st.session_state["messages"][-3:]:
            with st.chat_message(message["role"].lower()):
                st.write(message["content"])

def show_new_chat_page():
    st.title("Start New Conversation")
    
    with st.form("new_chat_form"):
        patient_history = st.text_area(
            "Patient History/Medical Background",
            help="Please provide relevant medical history, current medications, or any ongoing conditions.",
            height=150
        )
        
        medical_query = st.text_area(
            "Medical Question",
            help="What would you like to ask about?",
            height=100
        )
        
        submit_button = st.form_submit_button("Start Conversation")
        
        if submit_button:
            if not medical_query.strip():
                st.error("Please enter your medical question.")
                return

            set_chat_title(patient_history, medical_query)
            
            combined_message = f"Patient History:\n{patient_history}\n\nQuestion:\n{medical_query}"
            st.session_state["messages"] = [{"role": "user", "content": combined_message}]
            
            # Switch to conversation state
            st.session_state["page_state"] = "conversation"
            st.rerun()

def show_conversation_page():
    # Display chat title at the top
    st.title(st.session_state["chat_title"] or "Medical Consultation")
    
    # Chat history area with improved styling
    chat_container = st.container()
    with chat_container:
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"].lower()):
                st.markdown(message["content"])
    
    # Input area at the bottom
    st.divider()
    
    # Create two columns for text input and voice input
    col1, col2 = st.columns([8, 1])
    
    with col1:
        user_input = st.chat_input("Type your message...")
        if user_input:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            st.session_state["messages"].append({
                "role": "assistant",
                "content": "This is a placeholder response. Will be replaced with LLM response."
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
                st.session_state["messages"].append({
                    "role": "assistant",
                    "content": "This is a placeholder response. Will be replaced with LLM response."
                })
                st.rerun()
    
    with st.expander("📎 Upload Documents"):
        uploaded_file = st.file_uploader(
            "Upload medical documents (PDF/Image):", 
            type=["pdf", "jpg", "png"]
        )
        if uploaded_file:
            st.write(f"Uploaded: {uploaded_file.name}")

def get_sidebar():
    with st.sidebar:
        if st.button("New Chat", use_container_width=True):
            reset_chat_state()
            st.session_state["page_state"] = "new_chat"
            st.rerun()
        
        st.divider()
        
        st.subheader("Recent Chats")
        sample_chats = [
            {"id": f"chat_{i}", 
             "timestamp": f"2024-03-{i}", 
             "title": f"Medical Consultation {i}"} 
            for i in range(1, MAX_CHAT_HISTORY + 1)
        ]
        
        for chat in sample_chats:
            if st.button(
                f"💬 {chat['title']}\n{chat['timestamp']}", 
                key=chat['id'],
                use_container_width=True
            ):
                st.session_state["chat_title"] = chat['title']
                st.session_state["page_state"] = "conversation"
                st.rerun()
if st.session_state["page_state"] == "welcome":
    show_welcome_page()
elif st.session_state["page_state"] == "new_chat":
    show_new_chat_page()
elif st.session_state["page_state"] == "conversation":
    show_conversation_page()