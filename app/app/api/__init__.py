from flask.blueprints import Blueprint 
from .task import task_bp
from .feature import feature_bp

api = Blueprint('api', __name__)

api.register_blueprint(task_bp, url_prefix='/task')
api.register_blueprint(feature_bp, url_prefix='/feature')

