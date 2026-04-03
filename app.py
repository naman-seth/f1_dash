import streamlit as st
import requests
import time
import pandas as pd
import time

if "history" not in st.session_state:
    st.session_state.history = []

st.title("F1 dash")
'''dashdata = requests.get("http://127.0.0.1:8000/dashboard").json()
st.write(dashdata)'''

data = requests.get("http://127.0.0.1:8000/positions").json()
placeholder = st.empty()

table = []
for d in data[:10]:
    table.append({
            "Driver": d["driver_number"],
            "Position": d["position"],
        })
placeholder.table(table)


col1, col2 = st.columns(2)

with col1:
    st.subheader("Leaderboard")

with col2:
    st.subheader("Track Status")

st.session_state.history.append({
    "time": time.time(),
    "positions": {d["driver_number"]: d["position"] for d in data[:5]}
})

driver = list(st.session_state.history[0]["positions"].keys())[0]

times = []
positions = []

for entry in st.session_state.history:
    times.append(entry["time"])
    positions.append(entry["positions"][driver])

df = pd.DataFrame({
    "time": times,
    "position": positions
})

st.line_chart(df.set_index("time"))

'''df = pd.DataFrame(data[:10])
#df = df.sort_values("postion")
st.line_chart(df["position"])'''

time.sleep(2)
st.rerun()
'''table =[]
for d in data[:10]:
    table.append({
        "Driver": d["driver_number"],
        "Postions": d["position"]})
st.table(table)'''
