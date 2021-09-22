from celery import Celery 
from time import sleep

app = Celery(__name__, broker='redis://localhost:6379/0', backend='redis://127.0.0.1:6379/0')

@app.task
def mul(arg1, arg2):
    sleep(10)
    result = arg1 * arg2
    return result

def get_result(task_id):
    result = app.AsyncResult(task_id)
    return result.result
