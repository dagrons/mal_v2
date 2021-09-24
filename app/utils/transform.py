import os
import pefile
import array
import imageio
import numpy
from cfgexplorer import cfg_explore

def get_bytes_from_file(filepath, bytes_path, type='exe'):
    """
    从可执行文件中获取对应节段的数据(raw)
   
    :param filepath: filepath of executable 
    :param section_name: 
    :param type: executable type
    """
    if type == 'exe':
        with open(bytes_path, 'wb') as f:
            pe = pefile.PE(filepath)
            has_text = False
            for sec in pe.sections:
                if str(sec.Name).count('.text'):
                    f.write(sec.get_data())
                    has_text = True
            # !this may cause issue 
            if not has_text:
                for sec in pe.sections:
                    f.write(sec.get_data())

def get_gs_img(filepath, img_path):
    """
    返回可执行文件的灰度图像

    :param filepath:
    :param img_path:
    """
    with open(filepath, "rb") as f:
        filesize = os.path.getsize(filepath)
        width = 256 # 固定图片宽度为256
        rem = filesize%width
        a = array.array("B") # uint8数组
        a.fromfile(f, filesize-rem)
        g = numpy.reshape(a, (len(a)//width, width))
        g = numpy.uint8(g)
        imageio.imwrite(img_path, g)

def get_asm_from_bytes(bytes_path, asm_path):
    """
    对bytes文件反编译，获取对应的asm文件

    :param bytes_path:
    :param asm_path:
    """
    cmd_str = """ndisasm {} |""".format(bytes_path) + """awk '{{$1="";$2="";gsub(/^\s+|\s$/, "");print $1}}' > {}""" .format(asm_path)
    os.system(cmd_str)

def get_cfg_from_pe(binary_path, cfg_path):
    """
    generate cfg from binary

    :param binary_path: binary path
    :param cfg_path: generated cfg path with suffix .svg
    """
    cfg_explore(binary=binary_path, output=cfg_path)