import streamlit as st

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.sidebar.title("Past Conversations")
st.sidebar.write("Load past chats here!")

user_input = st.text_input("Ask a medical question:")
if st.button("Send"):
    st.session_state["messages"].append({"role": "User", "content": user_input})
    # Mock response
    st.session_state["messages"].append({"role": "Assistant", "content": "This is a sample response."})

for message in st.session_state["messages"]:
    st.write(f"{message['role']}: {message['content']}")
import openai

audio_file = st.file_uploader("Upload an audio file:", type=["mp3", "wav", "m4a"])
if audio_file:
    transcription = openai.Audio.transcribe("whisper-1", audio_file)
    st.write("Transcription:", transcription.get("text", ""))
search_query = st.sidebar.text_input("Search your chats")
if st.sidebar.button("Search"):
    # Implement a search function to retrieve matching results
    st.sidebar.write("Search results will appear here!")
uploaded_file = st.file_uploader("Upload a file (PDF/Image):", type=["pdf", "jpg", "png"])
if uploaded_file:
    st.write(f"Uploaded file: {uploaded_file.name}")
    # Save the file and associate it with a chat
