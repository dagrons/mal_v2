import tempfile
from flask.blueprints import Blueprint 
from flask import request, jsonify
from app import celery as celery_app
from redis import StrictRedis
from flask import current_app

from app.models.feature import *
from app.impl import task as taskImpl
from app.utils.is_pe import is_pe
from app.utils.compute_md5 import compute_md5

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/create', methods=['POST'])
def create():
    """
    用task_hash来保存当前的任务状态
    用lock:tl来控制对task_hash的互斥访问
    """    
    # compute md5 f the file 
    upload_file = request.files['file']
    id = compute_md5(upload_file)    
    if not is_pe(upload_file):
        return jsonify({
            'status': 'error',
            'msg': 'is not a pe file!',
            'filename': id
        })            
    if taskImpl.status(id) in ('running', 'done', 'reported'):
        return jsonify({
            'status': 'success',
            'msg': 'task finished',
            'filename': id
        })
    # check if task already exists
    redis_host = current_app.config['REDIS_HOST']
    redis_client = StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)        
    try:
        tl_lock = redis_client.setnx('lock:tl', 1) # lock for task list     
        if tl_lock:
            if not redis_client.hexists('task_hash', id):                                     
                # save file                                    
                u, upath = tempfile.mkstemp()                    
                with open(u, 'wb') as t:
                    t.write(upload_file.read())
                    upload_file.seek(0, 0)            
                    celery_app.submit.apply_async(args=[upath, id], task_id=id)                        
                    redis_client.hset('task_hash', id, 'PENDING')    
                    return jsonify({
                    'status': 'success',
                    'msg': 'task appended to the queue',
                    'filename': id
                    })
            else:
                return jsonify({
                    'status': 'success',
                    'msg': 'task already appended to the queue',
                    'filename': id
                })
    finally:                
        redis_client.delete('lock:tl')        
    return id

@task_bp.route('/status/<id>')
def status(id):
    return taskImpl.status(id)

@task_bp.route('/left_cnt')
def left_cnt():    
    return str(taskImpl.left_cnt())

@task_bp.route('/pending_cnt')
def pending_cnt():
    return str(taskImpl.pending_cnt())       
    
@task_bp.route('/running_list')
def running_list():
    return jsonify(taskImpl.running_list())     

@task_bp.route('/pending_list')
def pending_list():    
    return jsonify(taskImpl.pending_list())