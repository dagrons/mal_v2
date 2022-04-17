from app.models.feature import *

# sanity_correct
def sanity_correct(d, k):
    # 树形dfs遍历json报告
    if type(d[k]) == str:
        try:
            d[k] = d[k].encode(
                'utf-16', 'surrogatepass').decode('utf-16')
        except UnicodeDecodeError:
            d[k] = ascii(d[k])
            pass
    elif type(d[k]) == list:
        for i in range(len(d[k])):
                sanity_correct(d[k], i)
    elif type(d[k]) == dict:
        for i in d[k].keys():
            sanity_correct(d[k], i)
    else:
        return

# 预处理响应沙箱报告文件到res中
def preprocessing(res, report):

    res.info = Info()
    res.info.package = report['info']['package']
    res.info.platform = report['info']['platform']

    res.target = Target()
    res.target.md5 = report['target']['file']['md5']
    res.target.urls = report['target']['file']['urls']
    res.target.name = report['target']['file']['name']

    res.static = Static()
    res.static.strings = report['strings']
    res.static.pe_imports = report['static']['pe_imports']
    res.static.pe_exports = report['static']['pe_exports']
    res.static.pe_resources = report['static']['pe_resources']
    res.static.pe_sections = report['static']['pe_sections']
    if 'pe_timestamp' in report['static']:
        res.static.pe_timestamp = datetime.datetime.strptime(
            report['static']['pe_timestamp'], '%Y-%m-%d %H:%M:%S')
    else:
        res.static.pe_timestamp = datetime.datetime.now()

    try:
        res.procmemory = report['procmemory']
    except KeyError:    # procmemory为可选字段
        pass

    try:
        res._buffer = report['buffer']
    except KeyError:    # buffer为可选字段
        pass

    try:
        res.behavior = Behavior()
        res.behavior.generic = report['behavior']['generic']
        if len(report['behavior']['processes']) > 1 and len(report['behavior']['processes'][1]['calls']) > 1000:
            # 只要前1000个call, 不然文件可能很大
            report['behavior']['processes'][1]['calls'] = report['behavior']['processes'][1]['calls'][:1000]
        res.behavior.processes = report['behavior']['processes']
        res.behavior.processtree = report['behavior']['processtree']
    except KeyError:    # behavior为可选字段            
        pass

    for ops in ['file_opened', 'file_created', 'file_recreated', 'file_read', 'file_written', 'file_failed', 'directory_created', 'dll_loaded', 'mutex', 'regkey_opened', 'regkey_read', 'regkey_written', 'command_line', 'guid', 'extracted', 'dropped']:
        try:
            setattr(res.behavior, ops,
                    report['behavior']['summary'][ops])
        except KeyError:
            pass            # 忽略缺失字段
    try:
        res.signatures = report['signatures']
    except KeyError:    # signature为可选字段
        pass

    res.network = report['network']
    res.debug = report['debug']
