import os
import zipfile
from loguru import logger
 
 
def zip_reports(dirpath, fullname):
    """
    压缩指定文件夹到指定目录下
    :param dirpath: 需要打包的目标文件夹路径
    :param fullname: 压缩文件保存路径+xxxx.zip
    :return:
    """
    zip_files = zipfile.ZipFile(fullname, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):
        # 去掉目标根路径，只对目标文件夹下的文件及文件夹压缩
        fpath = path.replace(dirpath, '')
        for filename in filenames:
            zip_files.write(os.path.join(path, filename), os.path.join(fpath, filename))
    zip_files.close()
    logger.info("已经把文件夹{0}已压缩为{1}！".format(dirpath, fullname))
