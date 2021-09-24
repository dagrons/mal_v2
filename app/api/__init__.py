from flask.blueprints import Blueprint 
from app import celery as celery_app
from .task import task_bp

api = Blueprint('api', __name__)

api.register_blueprint(task_bp, url_prefix='/task')

