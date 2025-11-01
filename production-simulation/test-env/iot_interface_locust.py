from locust import HttpUser, User, task, between, events
import random
import json
import time

class ApiUser(HttpUser):
    """
    This user simulates REST API interactions:
    - Register
    - Login
    - Profile fetch
    - Device CRUD operations
    """
    host = "http://localhost:8080"  # Change this if your API runs on a different host/port
    wait_time = between(1, 3)

    def on_start(self):
        """
        Called when a simulated user is spawned.
        We try to login (or register if needed).
        """
        # Try login
        login_payload = {
            "email": "jeromel@gmail.com",
            "password": "password"
        }
        resp = self.client.post("/api/login", json=login_payload, name="Login")
        if resp.status_code == 200:
            data = resp.json()
            self.token = data.get("token")
        else:
            # If login failed, try to register
            reg_payload = {
                "email": login_payload["email"],
                "password": login_payload["password"]
            }
            resp2 = self.client.post("/api/register", json=reg_payload, name="Register")
            if resp2.status_code == 201:
                # after registration, login again
                resp3 = self.client.post("/api/login", json=login_payload, name="LoginAfterRegister")
                if resp3.status_code == 200:
                    self.token = resp3.json().get("token")
                else:
                    print("Login failed after registration", resp3.status_code, resp3.text)
            else:
                print("Failed to register", resp2.status_code, resp2.text)

    def _auth_headers(self):
        """Helper: returns headers including Authorization if token present."""
        headers = {}
        if hasattr(self, "token") and self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        headers["Content-Type"] = "application/json"
        return headers

    @task(1)
    def fetch_profile(self):
        self.client.get("/api/profile", headers=self._auth_headers(), name="Get Profile")

    @task(2)
    def register_device(self):
        """
        Simulate creating / registering a new device.
        """
        payload = {
            "device_id": f"dev-{random.randint(1000,9999)}",
            "name": "DeviceName",
            "type": "standard",
            "ui_type": "live_data",
            "properties": [
                {
                    "name": "Power",
                    "dataType": "bool",
                    "uiType": "toggle",
                    "defaultValue": False
                },
                {
                    "name": "Data",
                    "dataType": "string",
                    "uiType": "live_data",
                    "minValue": 0,
                    "maxValue": 100,
                    "defaultValue": 50
                }
            ]
        }
        self.client.post("/api/device/register", json=payload, headers=self._auth_headers(), name="Register Device")

    @task(3)
    def list_devices(self):
        self.client.get("/api/device/list", headers=self._auth_headers(), name="List Devices")

    @task(2)
    def show_device(self):
        # Randomly pick an ID (in real scenario, use existing device IDs)
        dev_id = random.randint(1, 10)
        self.client.get(f"/api/device/show/{dev_id}", headers=self._auth_headers(), name="Show Device")

    @task(2)
    def update_device_status(self):
        payload = {
            "device_id": "device_green",
            "status": random.choice(["Online", "offline"])
        }
        self.client.post("/api/device/update", json=payload, headers=self._auth_headers(), name="Update Device")

    @task(1)
    def delete_device(self):
        dev_id = random.randint(1, 10)
        self.client.delete(f"/api/device/delete/{dev_id}", headers=self._auth_headers(), name="Delete Device")

