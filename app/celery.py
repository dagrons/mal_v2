import tempfile
import time
import requests
import sys
import os
from celery import Celery 
from py2neo import Graph

from app.config import config
from app.models.feature import *
from app.utils.transform import get_asm_from_bytes, get_bytes_from_file
from app.utils.malware_classification.scripts.transform import pe2bmp
from app.utils.malware_classification.predict import predict as predict_cls
from app.utils.malware_sim.predict import predict as predict_sim
from app.utils.to_neo4j import to_neo4j
from app.utils.processing_report import sanity_correct, preprocessing

def make_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')    
    conf = config[config_name]        
    app = Celery(__name__, broker=conf.CELERY_BROKER_URL, backend=conf.CELERY_BROKER_BACKEND)    
    app.config_from_object(conf)      
    setattr(app, 'config', conf)    
    return app

app = make_app()

@app.task
def submit(f, id):
    """
    :param f: file path
    :param id: task id
    """    
    try:         
        connect(**app.config.MONGODB_SETTINGS)    
        g = Graph(app.config.NEO4J_SETTINGS['url'], auth=(app.config.NEO4J_SETTINGS['username'], app.config.NEO4J_SETTINGS['password']))  

        res = Feature(task_id=id)
        with open(f, 'rb') as fp:
            res.upload.put(fp)

        upath = f  
        af, afpath = tempfile.mkstemp(
            suffix='.asm') 
        bf, bfpath = tempfile.mkstemp(suffix='.bytes')
        pf, pfpath = tempfile.mkstemp(suffix='.bmp')

        get_bytes_from_file(upath, bfpath)  
        get_asm_from_bytes(bfpath, afpath)  
        pe2bmp(upath, pfpath) 

        res.local = Local()

        res.local.asm_file.put(open(af, 'rb'))
        res.local.bytes_file.put(open(bf, 'rb'))
        res.local.bmp_file.put(open(pf, 'rb'))

        res.local.malware_classification_resnet34 = predict_cls(
            pfpath)
        res.local.malware_sim_doc2vec = predict_sim(bfpath)

        # 将概率列表转化为概率字典
        t = {}
        prob_families = ['Ramnit', 'Lollipop', 'Kelihos_ver3', 'Vundo',
                            'Simda', 'Tracur', 'Kelihos_ver1', 'Obfuscator', 'Gatak']
        for k, v in zip(prob_families, res.local.malware_classification_resnet34):
            t[k] = v
        res.local.malware_classification_resnet34 = t    
                
        # 上传任务到cuckoo
        file = {"file": (res.task_id, res.upload)}
        headers = {
            "Authorization": app.config.CUCKOO_TOKEN}
        r = requests.post(
            app.config.CUCKOO_URL +
            '/tasks/create/file',
            files=file,
            headers=headers)
        cuckoo_task_id = str(r.json()['task_id'])        

        # 轮询获取报告
        done = False
        while not done:
            time.sleep(3)        
            r = requests.get(
                app.config.CUCKOO_URL +
                '/tasks/view/' + str(cuckoo_task_id),
                headers=headers)        
            if r.json()['task']['status'] == "reported":
                done = True        

        cuckoo_report = requests.get(
            app.config.CUCKOO_URL +
            '/tasks/report/' + str(cuckoo_task_id),
            headers=headers).json()        
        
        # 预处理报告
        sanity_correct({'report': cuckoo_report}, 'report')            
        preprocessing(res, cuckoo_report)           

        to_neo4j(g, res.to_json(), id)  # 保存结果到Neo4J    
        res.validate()        
        res.save()  # 保存结果到mongodb                    
    finally:
        disconnect()
