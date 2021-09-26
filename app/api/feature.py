from flask import Blueprint, jsonify
import numpy as np
from collections import Counter

from app.models.feature import *
from app.impl import task as taskImpl
from app.impl import feature as featureImpl

feature_bp = Blueprint('feature_bp', __name__)

@feature_bp.route('/dashboard')
def dashboard():
    return jsonify(featureImpl.dashboard())

@feature_bp.route('/get_apt_distribution')
def get_apt_distribution():        
    return jsonify(featureImpl.get_apt_distribution())

@feature_bp.route('/report/get/<id>')
def get_report(id):
    """
    get the result of a reported task
    if not reported, return None
    NOTE: the most 5 similar malware samples was computed 

    :param id: task id
    :return: result if task reported else None
    """    
    res = taskImpl.status(id)
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
        report = featureImpl.get_report(id)
        five_most_like = featureImpl.top_5_similar(
            report.local.malware_sim_doc2vec)
        return jsonify({
            'status': 'reported',
            'msg': 'reported',
            'isvalid': True,
            'report': report,
            'five_most_like': five_most_like
        })

@feature_bp.route('/png/get/<id>')
def get_png(self, filename):
    """
    get the png file of task
    if task id does not exist, return None

    :param filename: task id
    :return: None or file
    """
    if len(Feature.objects(task_id=filename)) < 1:
        abort(404)
    else:
        return Feature.objects(task_id=filename).first().local.bmp_file    
