import streamlit as st
from time import sleep

if "user_service" not in st.session_state or "user" not in st.session_state:
    st.error("Unexpected error. Please login again.")
    st.switch_page("pages/login.py")
else:
    user_service = st.session_state["user_service"]
    user = st.session_state["user"]

    st.title("Register New User")

    with st.form(key="user_registration_form"):
        name = st.text_input("Name", value=user.get("name", ""))
        email = st.text_input("Email", value=user.get("email", ""), disabled=True)
        organization = st.text_input("Organization", value=user.get("organization", ""))

        submit_button = st.form_submit_button("Submit")

    if submit_button:
        updates = {
            "name": name,
            "organization": organization,
        }
        user_id = user["user_id"]

        try:
            user_service.update_user(user_id, updates)
            st.success("User information updated successfully.")
            updated_user = user_service.get_user_by_id(user_id)
            st.session_state["user"] = updated_user
            sleep(1)
            st.switch_page("main.py")
        except Exception as e:
            st.error(f"An error occurred while updating user information: {str(e)}")
