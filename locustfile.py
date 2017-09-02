from uuid import uuid4
import json

from locust import HttpLocust, TaskSet, task

class UserBehavior(TaskSet):

    @task(2)
    def create(self):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

        data = {
            "task": "Testing {}".format(str(uuid4))
        }

        self.client.post("/todos/", json.dumps(data), headers=headers)

    @task(1)
    def list(self):
        self.client.get("/todos/")

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
