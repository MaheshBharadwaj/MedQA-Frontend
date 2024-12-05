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

st.set_page_config(page_title="SurgiChoice")

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
        with st.expander("See error"):
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


user = st.session_state["user"]
st.title(f"Welcome to SurgiChoice, {user['name']}!")
st.write("""
👋 Welcome to your medical assistant! I'm here to help answer your medical questions 
and provide reliable information based on your health history and concerns.

To get started:
- Click 'New Chat' in the sidebar to begin a new conversation
- Or select a recent chat to continue a previous discussion
""")
    
last_chat = chat_service.get_user_chats(limit=1)["chats"]
if not last_chat:
    st.stop()
else:
    last_chat = last_chat[0]
if st.button("Continue Last Chat"):
    st.session_state["current_chat_id"] = last_chat["chat_id"]
    st.switch_page("pages/chat.py")