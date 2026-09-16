from fastapi import FastAPI, HTTPException

app = FastAPI()

readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True},
    {"name": "hall-lamp",  "room": "hall",    "temp": 26.1, "online": True},
    {"name": "attic",      "room": "attic",   "temp": 31.9, "online": True},
    {"name": "fridge",     "room": "kitchen", "temp": 4.2,  "online": False},
    {"name": "patio",      "room": "outside", "temp": 29.8, "online": True},
]

def average_temp(devices):
    return sum(device['temp'] for device in devices) / len(devices)

print(average_temp(readings))

def hottest_device(devices):
    return max(devices, key=lambda device: device['temp'])

@app.get("/devices")
def get_devices():
    return readings

@app.get("/devices/hottest")
def get_hottest_device():
    return hottest_device(readings)

@app.get("/devices/online")
def get_online_devices():
    return [device for device in readings if device['online']]

@app.get("/devices/{name}")
def get_device(name: str):
    for device in readings:
        if device["name"] == name:
            return device
    raise HTTPException(status_code=404, detail="Device not found")