import requests
import time

url = "https://api.openf1.org/v1/position?session_key=11253"

response = requests.get(url)
data = response.json()

# print(type(data))
# print(data.keys())
# data = data["detail"]   # extract list

for d in data[:5]:
    print(d)

print(data[:2])  # show sample
for d in data[:10]:
    print({
        "driver": d.get("driver_number"),
        "position": d.get("position"),
        "time": d.get("date")
        })

current_state = {}

for d in data:
    driver = d["driver_number"]
    current_state[driver] = {
        "position": d["position"],
        "time": d["date"]
    }
'''while True:
    response = requests.get(url)
    data = response.json()

    print("Updated positions:")
    for d in data[:5]:
        print(d["driver_number"], d["position"])

    print("------")
    time.sleep(3)'''
'''
import requests

url = "https://api.openf1.org/v1/position?session_key=11253"

response = requests.get(url)

if response.status_code != 200:
    print("HTTP Error:", response.status_code)
else:
    data = response.json()

    if isinstance(data, list):
        for d in data[:5]:
            print(d.get("driver_number"), d.get("position"))

    else:
        print("API returned error:", data)
    '''
