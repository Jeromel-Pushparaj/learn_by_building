from locust import HttpUser, task, between
import random

class SpringBootUser(HttpUser):
    wait_time = between(1, 2)        # seconds between each task

    # 🔹 Task 1: GET all users
    @task(2)
    def get_all_users(self):
        self.client.get("/api/users")

    # 🔹 Task 2: POST (Create a new user)
    @task(1)
    def create_user(self):
        payload = {
            "userName": f"User{random.randint(100,999)}",
            "userRole": f"user{random.randint(100,999)}@example.com"
        }
        headers = {"Content-Type": "application/json"}
        self.client.post("/api/users", json=payload, headers=headers)

    # 🔹 Task 3: GET one user by ID (simulate random user)
    @task(1)
    def get_user_by_id(self):
        user_id = random.randint(1, 100)  # assuming IDs 1–10 exist
        self.client.get(f"/api/users/{user_id}")

    # 🔹 Task 4: DELETE a user (simulated)
    @task(1)
    def delete_user(self):
        user_id = random.randint(1, 10)
        self.client.delete(f"/api/users/{user_id}")
 
