import streamlit as st
from google_auth_oauthlib.flow import Flow
from constants import CLIENT_SECRETS_FILE, SCOPES, REDIRECT_URI



flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES, redirect_uri=REDIRECT_URI)
auth_url, _state = flow.authorization_url(access_type='offline')
html_content = f"""
        <div style="display: flex; justify-content: center;">
            <a href="{auth_url}" target="_self" style="background-color: '#fff' !force; color: '#000' !force ; text-decoration: none; text-align: center; font-size: 16px; margin: 4px 2px; cursor: pointer; padding: 8px 12px; border-radius: 4px; display: flex; align-items: center;">
                <img src="https://lh3.googleusercontent.com/COxitqgJr1sJnIDe8-jiKhxDx1FrYbtRHKJ9z_hELisAlapwE9LUPh6fcXIfb5vwpbMl4xl9H9TRFPc5NOO8Sb3VSgIBrfRYvW6cUA" alt="Google logo" style="margin-right: 8px; width: 26px; height: 26px; background-color: white; border: 2px solid white; border-radius: 4px;">
                Sign in with Google
            </a>
        </div>
        """

st.title("Welcome to Medical QA Assistant")
st.divider()
st.markdown("### Login with Google")
st.markdown(html_content, unsafe_allow_html=True)

