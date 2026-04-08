import streamlit as st
import requests
import time
import pandas as pd
import time

if "history" not in st.session_state:
    st.session_state.history = []

st.title("F1 dash")
track=requests.get("http://127.0.0.1:8000/track-status").json()
left, right = st.columns([1,1])

with left:
    st.subheader("🚦 Track Status")
with right:
    status = track.get("flag",'UNKNOWN')

    if status == "GREEN":
        st.success("🟢 GREEN FLAG")
    elif status == "YELLOW":
        st.warning("🟡 YELLOW FLAG")
    elif status == "RED":
        st.error("🔴 RED FLAG")
    elif status == "SC":
        st.info("🚗 SAFETY CAR")
    elif status == "VSC":
        st.info("⚠️ VIRTUAL SAFETY CAR")
    else:
        st.info(track.get('message'))

#dashdata = requests.get("http://127.0.0.1:8000/dashboard").json()
#st.write(dashdata)
fastest = requests.get("http://127.0.0.1:8000/fastest-lap").json()

driver = fastest.get("driver", "N/A")
lap_duration = fastest.get("lap_duration", 'None')
c1, c2 = st.columns([1,1])
with c1:
    st.subheader("Fastest Lap")
with c2:
    st.markdown(f"""
    <div style="
        background-color: #F3E8FF;
        padding: 12px;
        color: black;
        font-weight: 500;
    ">
       {driver} - {lap_duration} 
    </div>
    """, unsafe_allow_html=True)

data = requests.get("http://127.0.0.1:8000/positions").json()
# placeholder = st.empty()
table = []
for d in data[:10]:
    table.append({
            "Driver": d["driver_number"],
            "Position": d["position"],
            "Gap": d.get("gap", "-"),
            "Tyre": "M",  # placeholder
        })
st.table(table)
#placeholder.table(table)


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

'''col3=st.column(1)
with col3:'''
st.subheader("Race info")
st.metric('Lap','23/58')
st.metric('Session','Race')
st.metric('Track temp','32.3')

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
