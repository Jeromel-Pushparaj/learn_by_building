from locust import User, task, between
import paho.mqtt.client as mqtt
import time
import random

class MQTTUser(User):
    wait_time = between(1, 5)  # simulate idle time between actions

    def on_start(self):
        unique_id = f"client-{self.environment.runner.user_count}-{random.randint(1, 100000)}"
        self.client = mqtt.Client(client_id=unique_id)
        self.client.connect("192.168.1.12", 1883, 60)
        self.client.loop_start()

    @task
    def publish_message(self):
        topic = "device/device_green/brightness"
        payload = 10 
        self.client.publish(topic, payload)

    @task
    def publish_message(self):
        topic = "device/device_blue/brightness"
        payload = 15 
        self.client.publish(topic, payload)
    @task
    def subscribe_and_receive_status(self):
        def on_message(client, userdata, msg):
            print(f"Received: {msg.topic} {msg.payload.decode()}")

        self.client.subscribe("device/device_green/status")
        self.client.on_message = on_message
        time.sleep(1)
    @task
    def subscribe_and_receive_livedata(self):
        def on_message(client, userdata, msg):
            print(f"Received: {msg.topic} {msg.payload.decode()}")

        self.client.subscribe("device/device_temp/livedata")
        self.client.on_message = on_message
        time.sleep(1)

