import streamlit as st
import requests

st.title("F1 dash")
data = requests.get("http://127.0.0.1:8000/dashboard").json()
st.write(data)
