import streamlit as st
from streamlit_mic_recorder import mic_recorder
import openai
import requests
from constants import MAX_CHAT_HISTORY, OPENAI_API_KEY, LOGIN_URL, BACKEND_URL
from sidebar import get_sidebar
from utils import *
from datetime import datetime
from time import sleep

from services import *

openai.api_key = OPENAI_API_KEY
openai_client = openai.Client()

from google_auth_oauthlib.flow import Flow
from constants import CLIENT_SECRETS_FILE, SCOPES, REDIRECT_URI, BACKEND_URL

st.set_page_config(page_title="Medical QA Assistant")

if not st.session_state.get("user_service"):
    user_service = UserService(BACKEND_URL)
    st.session_state["user_service"] = user_service
else:
    user_service = st.session_state["user_service"]

if not st.session_state.get("chat_service"):
    chat_service = ChatService(BACKEND_URL)
    st.session_state["chat_service"] = chat_service
else:
    chat_service = st.session_state["chat_service"]

if not st.session_state.get("file_service"):
    file_service = FileService(BACKEND_URL)
    st.session_state["file_service"] = file_service
else:
    file_service = st.session_state["file_service"]

if not st.session_state.get("llm_service"):
    llm_service = LLMService(BACKEND_URL)
    st.session_state["llm_service"] = llm_service
else:
    llm_service = st.session_state["llm_service"]

if st.query_params.get("code"):
    auth_code = st.query_params.get('code')
    st.query_params.clear()
    flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
    auth = flow.fetch_token(code=auth_code)
    id_token = auth['id_token']
    response = requests.post(f"{LOGIN_URL}", json={"code": id_token})
    if response.status_code != 200:
        st.error("Error logging in. Please try again!")
        with st.expander:
            st.write(response.text)
        st.stop()
    response = response.json()
    token = response["access_token"]
    user_service.set_auth_token(token)
    chat_service.set_auth_token(token)
    file_service.set_auth_token(token)
    # message_service.set_auth_token(token)
    llm_service.set_auth_token(token)
    user = response["user"]
    st.session_state["user"] = user
    st.session_state["token"] = token

    if not user["name"]:
        st.switch_page("pages/register.py")

    st.info(f"Login successfull!")
    sleep(0.7)
    st.rerun()

if st.session_state.get("user") is None:
    st.switch_page("pages/login.py")

get_sidebar()

if "openai_client" not in st.session_state:
    st.session_state["openai_client"] = openai_client
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "page_state" not in st.session_state:
    st.session_state["page_state"] = "welcome"
if "chat_title" not in st.session_state:
    st.session_state["chat_title"] = None


def reset_chat_state():
    st.session_state["messages"] = []
    st.session_state["chat_title"] = None

def show_welcome_page():
    user = st.session_state["user"]
    st.title(f"Welcome to Medical QA Assistant, {user['name']}!")
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
    patient_history = st.text_area(
        "Patient History/Medical Background",
        value=st.session_state.get("patient_history", ""),
        height=150
    )
    audio = mic_recorder(
        start_prompt="Record Notes 🎤",
        stop_prompt="Stop ⏹️",
        just_once=True,
        use_container_width=True
    )
    if audio:
        patient_data = speech_to_text(audio)
        st.session_state["patient_history"] = patient_data
        st.rerun()

    
    medical_query = st.text_area(
        "Medical Question",
        help="What would you like to ask about?",
        value="Is this patient appropriate for inpatient or out patient surgery?",
        height=100
    )
    
    submit_button = st.button("Start Conversation")
        
    if submit_button:
        if not medical_query.strip():
            st.error("Please enter your medical question.")
            return

        set_chat_title(patient_history, medical_query)
        
        combined_message = f"Patient History:\n{patient_history}\n\nQuestion:\n{medical_query}"
        st.session_state["messages"] = [{"role": "user", "content": combined_message}]
        chat_service.create_chat(st.session_state["chat_title"], "gpt")
        st.session_state["page_state"] = "conversation"
        st.rerun()

def show_conversation_page():
    st.title(st.session_state["chat_title"] or "Medical Consultation")
    st.session_state["patient_history"] = None
    chat_container = st.container()
    with chat_container:
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"].lower()):
                st.markdown(message["content"])
    
    st.divider()
    
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