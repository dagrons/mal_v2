import numpy as np

from app.models.feature import *
from app.handler import task as task_handler


def dashboard():
    """
    首页数据接口
    """
    res = {'samples_count': Feature.objects.count(), 'current_count': task_handler.left_cnt(),
           'recent_count': Feature.objects(upload_time__gte=datetime.datetime.utcnow(
           ) - datetime.timedelta(days=7)).count()}

    # for counting

    # for family distribution
    type_res = {}
    for type in ['Ramnit', 'Lollipop', 'Kelihos_ver3', 'Vundo', 'Simda', 'Tracur', 'Kelihos_ver1', 'Obfuscator',
                 'Gatak']:
        type_res[type] = 0

    all_locals = Feature.objects.only(
        'local.malware_classification_resnet34')
    for t in all_locals:
        max_type = None
        for type in ['Ramnit', 'Lollipop', 'Kelihos_ver3', 'Vundo', 'Simda', 'Tracur', 'Kelihos_ver1', 'Obfuscator',
                     'Gatak']:
            if max_type is None or t.local.malware_classification_resnet34[type] >= \
                    t.local.malware_classification_resnet34[max_type]:
                max_type = type
        type_res[max_type] += 1
    res['type_res'] = type_res

    # for trend area
    trend_area = []
    year_ranges = []
    end_of_range = datetime.datetime.today().date()  # 到xx年
    for t in range(20):
        year_ranges.append(end_of_range - datetime.timedelta(days=365 * t))
    year_ranges.reverse()

    ts = Feature.objects().only('static.pe_timestamp')
    for y in year_ranges:
        cnt = 0
        for t in ts:
            if t.static.pe_timestamp.date() <= y:
                cnt += 1
        trend_area.append({"year": str(y), "value": cnt})
    res['trend_area'] = trend_area

    return res


def get_report(id):
    """
    获取某个样本的分析报告
    get the result of a reported task
    if not reported, return None
    NOTE: the most 5 similar malware samples was computed 

    :param id: task id
    :return: result if task reported else None
    """
    if len(Feature.objects(task_id=id)) >= 1:
        return Feature.objects(task_id=id).first()
    else:
        return None


def top_5_similar(vec):
    """
    获取vec相似度最高的5个向量对应的恶意样本md5
    这里每次都会把所有数据拉出来计算，复杂度非常高

    :param vec: the doc2vec of the malware
    :return: the most five similar malwares id
    """
    ts = Feature.objects.only('task_id').only('local.malware_sim_doc2vec').only('apt_family')
    sims = []

    for t in ts:
        vec2 = np.array(t.local.malware_sim_doc2vec)
        sims.append((t.task_id, np.sqrt(np.sum(np.square(vec - vec2))), t.apt_family))
    sims = sorted(sims, key=lambda x: -x[1])
    return [t for t in sims[1:7] if t[1] != 1]  # 跳过自己


def get_apt_distribution():
    """获取apt的统计分布"""
    type_res = {}
    for type in ["APT_28", "APT_29", "Dark_Hotel", "Energetic_Bear", "Equation_Group", "Gorgon_Group"]:
        type_res[type] = 0

    all_apts = Feature.objects.only("apt_family")
    for t in all_apts:
        for k in ["APT_28", "APT_29", "Dark_Hotel", "Energetic_Bear", "Equation_Group", "Gorgon_Group"]:
            if t.apt_family == k:
                type_res[k] += 1
                break
    return type_res
