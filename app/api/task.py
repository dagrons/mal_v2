import tempfile
from flask.blueprints import Blueprint 
from flask import request
from app import celery as celery_app
from redis import StrictRedis

from app.utils.compute_md5 import compute_md5

task_bp = Blueprint('task_bp', __name__)

@task_bp.route('/create', methods=['POST'])
def create():
    # compute md5 f the file 
    upload_file = request.files['file']
    id = compute_md5(upload_file)
    # check if task already exists
    redis_client = StrictRedis(decode_responses=True)
    import pdb; pdb.set_trace()
    tl_lock = redis_client.setnx('lock:tl', 1) # lock for task list 
    if tl_lock:
        if not redis_client.hexists('task_hash', id):         
            redis_client.hset('task_hash', id, 'PENDING')                    
            # save file                                    
            u, upath = tempfile.mkstemp()    
            with open(u, 'wb') as t:
                t.write(upload_file.read())
                upload_file.seek(0, 0)            
                celery_app.submit.apply_async(args=[upath, id], task_id=id)                        
        redis_client.delete('lock:tl')        
    return id


