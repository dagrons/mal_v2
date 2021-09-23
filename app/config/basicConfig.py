import os
from dotenv import load_dotenv

load_dotenv()

class basicConfig():    
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379/0')
    CELERY_BROKER_BACKEND = os.getenv('CELERY_BROKER_BACKEND', 'redis://127.0.0.1:6379/0')
    MONGODB_SETTINGS = {
        'db': os.getenv('MONGO_DBNAME', 'mal'),
        'host': os.getenv('MONGO_HOST', 'mongo'),
        'port': os.getenv('MONGO_PORT',  27017),
        'username': os.getenv('MONGO_USERNAME', 'mongoadmin'),
        'password': os.getenv('MONGO_PASSWORD', 'mongoadmin'),
        'authentication_source': os.getenv('MONGO_AUTHDB', 'admin')
    }