from flask.blueprints import Blueprint 
from app import celery as celery_app

api = Blueprint('api', __name__)

@api.route('/mul/<arg1>/<arg2>')
def mul(arg1, arg2):
    result_id = celery_app.mul.delay(arg1, arg2)
    return str(result_id)
