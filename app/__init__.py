import os
from flask import Flask
from app.api import api

from .config import config

def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    register_extensions(app)    
    register_blueprints(app)        

    return app

def register_blueprints(app):        
    app.register_blueprint(api, url_prefix='/api')

def register_extensions(app):
    pass

