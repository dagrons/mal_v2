from flask.blueprints import Blueprint
import celery_app

api = Blueprint('api', __name__)

@api.route('/mul/<arg1>/<arg2>')
def _mul(arg1, arg2):
    result = celery_app.mul.delay(int(arg1), int(arg2))
    return result.id

@api.route('/get_result/<result_id>')
def _result(result_id):
    result = celery_app.get_result(result_id)
    return str(result)