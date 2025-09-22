import base64
import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def md5_str(args):
    """
    对字符串进行md5加密
    :param args: 需要加密的字段
    :return: 返回加密值
    """
    # 先把变量转成utf-8的编码格式
    args = str(args).encode('utf-8')
    # md5加密
    args_value = hashlib.md5(args).hexdigest()
    # 返回
    return args_value


def base64_encode(args):
    """
    base64加密，以指定的编码格式编码字符串
    :param args:
    :return:
    """
    # 先把变量转成utf-8的编码格式
    args = str(args).encode('utf-8')
    # base64加密
    base64_value = base64.b64encode(args).decode(encoding='utf-8')
    # 返回
    return base64_value


def base64_decode(content):
    """
    base64解密
    @return:
    """
    # 原文转为二进制
    content = str(content).encode("utf-8")
    # base64解密(二进制)
    decode_value = base64.b64decode(content)
    # 转成字符串
    encode_str = decode_value.decode("utf-8")
    return encode_str


def sha1_encode(params):
    """
    参数sha1加密
    @param params:
    @return:
    """
    enc_data = hashlib.sha1()
    enc_data.update(params.encode(encoding="utf-8"))
    return enc_data.hexdigest()


def dict_ascii_sort(args_dict):
    """
    把字典按照key的ASCII码升序排序
    @param args_dict:
    @return:
    """
    dict_key = dict(args_dict).keys()
    new_list = list(dict_key)
    new_list.sort()
    new_dict = {}
    for key in new_list:
        new_dict[key] = args_dict[key]
    return new_dict


def rsa_str(s):
    """
    对字符串进行rsa加密
    :param s: 需要加密的字段
    :return: 返回加密值
    """
    # 读取公钥信息内容
    public_key_str = open('datas/rsa_public_key.pem').read()
    # 导入公钥信息，返回公钥对象
    public_key = RSA.importKey(public_key_str)
    # 基于公钥创建RSA加密器对象
    pk = PKCS1_v1_5.new(public_key)
    # 进行加密（加密前数据转换为二进制格式）
    rsa_data = pk.encrypt(s.encode('utf-8'))
    # 进行base64编码
    base64_data = base64.b64encode(rsa_data)
    # 把数据由二进制转换为文本类型的
    return base64_data.decode('utf-8')
