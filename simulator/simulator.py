import os
import time
import random
import requests
from datetime import datetime, timezone


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
INTERVAL_SECONDS = float(os.getenv("SIM_INTERVAL_SECONDS", "2"))


DEVICES = [
    {
        "id": "ahu-001",
        "type": "air_handler",
        "temperature_range": (20.0, 25.0),
        "humidity_range": (35.0, 55.0),
    },
    {
        "id": "vav-001",
        "type": "vav_box    ",
        "temperature_range": (19.0, 24.0),
        "humidity_range": (30.0, 50.0),
    },
    {
        "id": "boiler-001",
        "type": "boiler",
        "temperature_range": (55.0, 75.0),
        "humidity_range": (20.0, 35.0),
    },
]


def register_device(device):
    payload = {
        "id": device["id"],
        "type": device["type"],
        "status": "online",
        "temperature": 0,
        "humidity": 0,
    }

    try:
        response = requests.post(f"{BACKEND_URL}/devices", json=payload, timeout=5)

        if response.status_code in (200, 201, 409):
            print(f"[REGISTERED] {device['id']}")
        else:
            print(f"[REGISTER FAILED] {device['id']} status={response.status_code} body={response.text}")

    except requests.RequestException as error:
        print(f"[REGISTER ERROR] {device['id']} error={error}")


def generate_telemetry(device, counter):
    temperature_min, temperature_max = device["temperature_range"]
    humidity_min, humidity_max = device["humidity_range"]

    status = "online"

    # Simulate occasional offline device
    if random.random() < 0.1:
        status = "offline"

    payload = {
        "device_id": device["id"],
        "status": status,
        "temperature": round(random.uniform(temperature_min, temperature_max), 2),
        "humidity": round(random.uniform(humidity_min, humidity_max), 2),
        "timestamp": datetime.now(timezone.utc).isoformat(),    
    }

    # Simulate bad firmware payload every 20th message
    if counter % 20 == 0:
        payload["temperature"] = "CORRUPTED_VALUE"

    return payload


def send_telemetry(payload):
    try:
        response = requests.post(f"{BACKEND_URL}/telemetry", json=payload, timeout=5)

        if response.status_code in (200, 201):
            print(f"[TELEMETRY OK] {payload}")
        else:
            print(f"[TELEMETRY REJECTED] status={response.status_code} body={response.text} payload={payload}")

    except requests.RequestException as error:
        print(f"[TELEMETRY ERROR] error={error} payload={payload}")


def wait_for_backend():
    print(f"[WAITING] backend={BACKEND_URL}")

    while True:
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=3)
            if response.status_code == 200:
                print("[BACKEND READY]")
                return
        except requests.RequestException:
            pass

        time.sleep(2)


def main():
    wait_for_backend()

    for device in DEVICES:
        register_device(device)

    counter = 1

    while True:
        for device in DEVICES:
            payload = generate_telemetry(device, counter)
            send_telemetry(payload)
            counter += 1

        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()