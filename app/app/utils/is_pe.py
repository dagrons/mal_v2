def is_pe(fp):

    flag1 = fp.read(2)  # 读取文件前两个字节
    fp.seek(0x3c)  # 获取PE头偏移
    offset = ord(fp.read(1))
    fp.seek(offset)
    flag2 = fp.read(4)  # 获取PE头签名
    fp.seek(0, 0)
    if flag1 == b'MZ' and flag2 == b'PE\x00\x00':  # 判断是否为PE文件的典型特征签名
        return True
    return False
