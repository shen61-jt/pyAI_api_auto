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


def read_test_result():
    """
    读取测试结果文件内容，支持多种编码尝试
    :return: 文件内容或错误信息
    """
    file_path = r"reports/result.txt"
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            logger.error(f"测试结果文件不存在: {file_path}")
            return "测试结果文件不存在"

        # 尝试不同的编码方式读取
        encodings = ['utf-8', 'gbk', 'gb2312', 'latin-1']
        for encoding in encodings:
            try:
                with open(file_path, "r", encoding=encoding) as f:
                    content = f.read()
                logger.info(f"成功使用 {encoding} 编码读取文件")
                return content
            except UnicodeDecodeError:
                continue

        # 如果所有编码都失败
        logger.error("无法使用任何编码读取文件")
        return "文件编码格式不支持"

    except Exception as e:
        logger.error(f"读取测试结果文件失败: {e}")
        return f"读取文件失败: {str(e)}"
