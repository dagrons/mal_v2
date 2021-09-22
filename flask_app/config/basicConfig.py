import os
from dotenv import load_dotenv

load_dotenv()

class basicConfig():    
    BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_BROKER_BACKEND', 'redis://127.0.0.1:6379/0')