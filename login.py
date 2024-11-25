import streamlit as st
from google_auth_oauthlib.flow import Flow

CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/userinfo.email"]
REDIRECT_URI = "http://localhost:8501"

flow = Flow.from_client_secrets_file(CLIENT_SECRETS_FILE, scopes=SCOPES)
flow.redirect_uri = REDIRECT_URI

auth_url, _ = flow.authorization_url(prompt="consent")
st.write(f"[Login with Google]({auth_url})")
