from fastapi import FastAPI
import requests
import time

app = FastAPI()

cache = {
    "data": None,
    "last_updated": 0
}
cache_fastest={
        'data': None,
        'last_updated':0
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
    data= requests.get("https://api.openf1.org/v1/race_control?session_key=11253").json()
    return data[-1] if data else{}
@app.get("/dashboard")
def dashboard():
    return {
        "positions": get_positions(),
        "laps": get_laps(),
        "track": track_status()
    }

@app.get("/fastest-lap")
def fastest_lap():
    import time,requests

    global cache_fastest

    if time.time() - cache_fastest['last_updated'] > 5:
        data = requests.get("https://api.openf1.org/v1/laps?session_key=11253").json()

        fastest = None
        min_time = float("inf")

        for lap in data:
            lap_duration = lap.get("lap_duration")

            if lap_duration is not None and lap_duration < min_time:
                min_time = lap_duration
                fastest = lap

        if fastest:
            cache_fastest["data"] = {
                "driver": fastest.get("driver_number"),
                "lap_duration": fastest.get("lap_duration")
            }

        cache_fastest['last_updated'] = time.time()
    return cache_fastest['data'] or {}

    
