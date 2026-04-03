from fastapi import FastAPI
import requests
import time

app = FastAPI()

cache = {
    "data": None,
    "last_updated": 0
}

@app.get("/")
def home():
    return {"message": "F1 Backend Running"}

@app.get("/positions")
def get_positions():
    global cache
    url = "https://api.openf1.org/v1/position?session_key=11253" #qualifying data
    data = requests.get(url).json()

    '''cleaned = []
    for d in data:
        cleaned.append({
            "driver": d.get("driver_number"),
            "position": d.get("position"),
            "time": d.get("date")
        })

    return cleaned'''
    if time.time() - cache["last_updated"] > 2:

        cache["data"] = data
        cache["last_updated"] = time.time()

    return cache["data"]
@app.get("/laps")
def get_laps():
    return requests.get("https://api.openf1.org/v1/laps?session_key=11253").json()

@app.get("/track-status")
def track_status():
    return requests.get("https://api.openf1.org/v1/race_control?session_key=11253").json()
@app.get("/dashboard")
def dashboard():
    return {
        "positions": get_positions(),
        "laps": get_laps(),
        "track": track_status()
    }
