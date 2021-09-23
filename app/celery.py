import os
from celery import Celery 

from .config import config

def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')    
    app = Celery(__name__, broker=config[config_name].CELERY_BROKER_URL, backend=config[config_name].CELERY_BROKER_BACKEND)    
    app.config_from_object(config[config_name])    
    return app

app = make_app()

@app.task 
def mul(arg1, arg2):
    from time import sleep
    sleep(10)
    return int(arg1) + int(arg2)
