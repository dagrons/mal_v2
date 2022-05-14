from flask import Blueprint, jsonify, send_file, abort

from app.models.feature import Feature
from app.handler import task as task_handler
from app.handler import feature as feature_handler

feature_bp = Blueprint('feature_bp', __name__)


@feature_bp.route('/dashboard')
def dashboard():
    return jsonify(feature_handler.dashboard())


@feature_bp.route('/get_apt_distribution')
def get_apt_distribution():
    return jsonify(feature_handler.get_apt_distribution())


@feature_bp.route('/report/get/<id>')
def get_report(id):
    """
    get the result of a reported task
    if not reported, return None
    NOTE: the most 5 similar malware samples was computed

    :param id: task id
    :return: result if task reported else None
    """
    res = task_handler.status(id)
    if res == "empty" or res == "exception":
        return jsonify({
            'status': 'error',
            'msg': 'the report do not exist or task meet an exception',
            'isvalid': False
        })
    elif res == "running" or res == "done":
        # if done but not reported, can be considered as running
        return jsonify({
            'status': 'running',
            'msg': 'the task is still running',
            'isvalid': True,
        })
    else:
        report = feature_handler.get_report(id)
        five_most_like = feature_handler.top_5_similar(
            report.local.malware_sim_doc2vec)
        return jsonify({
            'status': 'reported',
            'msg': 'reported',
            'isvalid': True,
            'report': report,
            'five_most_like': five_most_like
        })


@feature_bp.route('/bmp/get/<filename>')
def get_bmp(filename):
    """
    get the png file of task
    if task id does not exist, return None

    :param filename: task id
    :return: None or file
    """
    if len(Feature.objects(task_id=filename)) < 1:
        abort(404)
    else:
        return send_file(Feature.objects(task_id=filename).first().local.bmp_file,
                         attachment_filename=filename + '.bmp')
