from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task(400)
    def hello_world(self):
        self.client.get("/student-class/1/a/")

    def on_start(self):
        self.client.post(
            "/login/", json={"username": "teacher", "password": "Zzz123121"}
        )
