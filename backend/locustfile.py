from locust import HttpLocust, TaskSet, task

class LoadTask(TaskSet):
    def on_start(self):
        pass
    
    def on_stop(self):
        pass
    
    @task
    def index_page(self):
        self.client.get('/api/calendar/2020/01')

class WebsiteUser(HttpLocust):
    task_set = LoadTask
    min_wait = 3000
    max_wait = 8000