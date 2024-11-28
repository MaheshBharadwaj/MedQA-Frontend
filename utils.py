import tempfile
import streamlit as st
from pathlib import Path
from constants import CHAT_TITLE_PROMPT
from datetime import datetime

def speech_to_text(audio):
     openai_client = st.session_state.openai_client
     with tempfile.TemporaryDirectory() as temp_dir:
        temp_wav_path = f"{temp_dir}/temp.wav"
        with st.spinner():
            with open(temp_wav_path, "wb") as temp_wav_file:
                temp_wav_file.write(audio["bytes"])

            transcript = openai_client.audio.transcriptions.create(
                    model="whisper-1", file=Path(temp_wav_path)
            )
        prompt = transcript.text
        return prompt
     

def set_chat_title(patient_history, medical_query):
    try:
        openai_client = st.session_state["openai_client"]
        title_prompt = f"{CHAT_TITLE_PROMPT}\n\nPatient Information:\n{patient_history}\n\nMedical Query:\n{medical_query}"

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": "You are a medical title generator. Generate concise, descriptive titles for medical consultations."
            },
            {
                "role": "user",
                "content": title_prompt
            }],
            max_tokens=50,
            temperature=0.3
        )
        chat_title = response.choices[0].message.content.strip()
    except Exception as e:
        chat_title = f"Medical Consultation - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        st.toast("Failed to generate custom title. Using default format.")
    finally:
        st.session_state["chat_title"] = chat_title