import streamlit as st
from streamlit_mic_recorder import mic_recorder
from constants import DEFAULT_PATIENT_HISTORY
from utils import speech_to_text, set_chat_title
from sidebar import get_sidebar

get_sidebar()

st.title("Start New Conversation")

try:
    chat_service = st.session_state["chat_service"]
    # message_service = st.session_state["message_service"]
    llm_service = st.session_state["llm_service"]
except KeyError:
    st.switch_page("pages/login.py")

if "patient_history" not in st.session_state or st.session_state["patient_history"] is None:
    st.session_state["patient_history"] = DEFAULT_PATIENT_HISTORY
st.session_state["llm_mode"] = "RAG"

c1, c2 = st.columns([1, 1])
with c1:
    option = st.selectbox(
        "Version",
        ("RAG", "Vanilla"),
        index=0,
        placeholder="Select the variant",
    )
    if option == "Vanilla":
        st.session_state["llm_mode"] = "Vanilla"

with c2:
    provider = st.selectbox(
        "Provider",
        ("OpenAI", "Claude"),
        index=0,
        placeholder="Select the LLM provider",
        disabled=True,
        help="Currently only OpenAI is supported",
    )


patient_history = st.text_area(
    "Patient History/Medical Background",
    value=st.session_state["patient_history"],
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
    else:
        set_chat_title(patient_history, medical_query)
        chat = chat_service.create_chat(st.session_state["chat_title"], "gpt")
        chat_id = chat["chat_id"]
        combined_message = f"Patient History:\n{patient_history}\n\nQuestion:\n{medical_query}"
        chat_service.add_message(chat_id, "user", combined_message)
        st.session_state["messages"] = [{"role": "user", "content": combined_message}]
        mode = st.session_state["llm_mode"]
        try:
            response = llm_service.get_completion(st.session_state["messages"], mode=mode)["response"]
        except Exception as e:
            response = f"An error occurred! Please try again later"
            with st.expander("See error"):
                st.write(e)
        chat_service.add_message(chat_id, "ai", response)
        st.session_state["messages"].append({"role": "ai", "content": response})
        st.session_state["current_chat_id"] = chat_id
        st.session_state["patient_history"] = None
        st.switch_page("pages/chat.py")
