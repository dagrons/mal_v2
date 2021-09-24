import hashlib

def compute_md5(f):
    f_hash = hashlib.md5()
    line = f.readline()
    while (line):
        f_hash.update(line)
        line = f.readline()
    filename = f_hash.hexdigest()
    f.seek(0, 0)

    return filename

