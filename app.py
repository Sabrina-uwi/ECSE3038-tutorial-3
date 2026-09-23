from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Reading(BaseModel):
    name: str
    room: str
    temp: float
    online: bool

app = FastAPI()
    
readings = [
    {"name": "front-door", "room": "hall",    "temp": 27.4, "online": True, "colour": "red"},
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

#@app.get("/devices/{name}")
#def get_device(name: str):
#    for device in readings:
#        if device["name"] == name:
#           return device
#    raise HTTPException(status_code=404, detail="Device not found")

@app.get("/devices/{name}")
async def get_device(name: str):
    device = next((d for d in readings if d['name'] == name), None)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

@app.get("/stats")
def get_stats():
    return {
        "average_temperature": average_temp(readings),
    }

#@app.post("/device", status_code=201)
#async def add_reading(reading: Reading):

 #   for existing_reading in readings:
  #     if existing_reading["name"] == reading["name"]:
   #      raise HTTPException(status_code=400, detail="Reading with this name already exists")
    #
    #readings.append(reading)
    #return {"message": "Reading added successfully", "reading": reading}

@app.post("/devices", status_code=201)
async def add_device(device: Reading):
    reading_dict = device.model_dump()  # Convert Pydantic model to dictionary
    readings.append(reading_dict)
    return device

@app.get("/rooms/{room}/devices")
def get_devices_by_room(room: str):
    devices_in_room = [device for device in readings if device["room"] == room]
    if not devices_in_room:
        raise HTTPException(status_code=404, detail="No devices found in this room")
    return devices_in_room

@app.put("/devices/{name}")
async def update_device(name: str, updated_device: Reading):
    for index, device in enumerate(readings):
        if device["name"] == name:
            readings[index] = updated_device.model_dump()  # Update the device with new data
            return updated_device
    raise HTTPException(status_code=404, detail="Device not found")