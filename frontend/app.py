import requests
import streamlit as st

st.set_page_config(
    page_title="SupportPilot AI",
    page_icon="🤖",
)

st.title("SupportPilot AI")

backend_url = "http://backend:8000/health"

try:
    response = requests.get(backend_url, timeout=5)

    if response.status_code == 200:
        st.success("Backend connection: OK")
        st.json(response.json())
    else:
        st.error(f"Backend returned status {response.status_code}")

except requests.RequestException as e:
    st.error(f"Backend connection failed: {e}")