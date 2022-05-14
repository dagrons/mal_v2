from redis import StrictRedis
import os

from app.models.feature import Feature
from app.handler.task import *
from flask import current_app


def status(id):
    if len(Feature.objects(task_id=id)) >= 1:
        return "reported"
    redis_host = current_app.config['REDIS_HOST']
    redis_client = StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
    try:
        tl_lock = redis_client.setnx('lock:tl', 1)  # lock for task list
        if tl_lock:
            if redis_client.hexists('task_hash', id):
                if redis_client.hget('task_hash', id) == 'RUNNING' or redis_client.hget('task_hash', id) == 'PENDING':
                    return 'running'
                elif redis_client.hget('task_hash', id) == 'EXCEPTION':
                    return 'exception'
                else:
                    return 'done'
            else:
                return 'empty'
    finally:
        redis_client.delete('lock:tl')


def running_list():
    redis_host = current_app.config['REDIS_HOST']
    redis_client = StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
    try:
        tl_lock = redis_client.setnx('lock:tl', 1)  # lock for task list
        if tl_lock:
            task_hash = redis_client.hgetall('task_hash')
            return [k for k, v in task_hash.items() if v == 'RUNNING']
    finally:
        redis_client.delete('lock:tl')


def pending_list():
    redis_host = current_app.config['REDIS_HOST']
    redis_client = StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
    try:
        tl_lock = redis_client.setnx('lock:tl', 1)  # lock for task list
        if tl_lock:
            task_hash = redis_client.hgetall('task_hash')
            return [k for k, v in task_hash.items() if v == 'PENDING']
    finally:
        redis_client.delete('lock:tl')


def left_cnt():
    redis_host = current_app.config['REDIS_HOST']
    redis_client = StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
    try:
        tl_lock = redis_client.setnx('lock:tl', 1)  # lock for task list
        if tl_lock:
            task_hash = redis_client.hvals('task_hash')
            return len([x for x in task_hash if x == 'RUNNING'])
    finally:
        redis_client.delete('lock:tl')


def pending_cnt():
    redis_host = current_app.config['REDIS_HOST']
    redis_client = StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
    try:
        tl_lock = redis_client.setnx('lock:tl', 1)  # lock for task list
        if tl_lock:
            task_hash = redis_client.hvals('task_hash')
            return len([x for x in task_hash if x == 'PENDING'])
    finally:
        redis_client.delete('lock:tl')
