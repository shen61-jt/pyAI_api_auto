import json
import os
from string import Template
import allure
import jsonpath
import openpyxl
from loguru import logger
from requests import request
from common.handle_data import query_db
from openpyxl import Workbook

# 公共的数据容器-字典格式，用来保存接口之间要关联的字段
dic_env = {}


def read_excel(file_path, sheet_name):
    """
    读取Excel文件数据封装函数
    :param file_path: excel文件的路径
    :param sheet_name: 要读取sheet名称
    :return: 返回列表嵌套字典的数据结构
    """
    wb = openpyxl.load_workbook(file_path)
    # 得到sheet
    sh = wb[sheet_name]
    # 通过sheet获取所有的数据
    datas = list(sh.values)
    # 获取第一行的标题
    header = datas[0]
    new_li = []
    for i in datas[1:]:
        result = dict(zip(header, i))
        new_li.append(result)
    return new_li


def send_request(case):
    """
    统一发送请求封装
    :param case: 用例数据
    :return: 响应结果
    """
    # 提取所有请求字段
    case_id = case['用例编号']
    title = case['用例标题']
    method = case['请求方法']
    url = case['请求地址']
    params = case['请求参数']
    headers = case['请求头']
    # 在请求发送、记录请求日志之前做标记识别替换的动作，需要做参数替换有请求地址、请求参数、请求头
    if isinstance(url, str):
        url = Template(url).safe_substitute(dic_env)
    if params:
        params = Template(params).safe_substitute(dic_env)
    if headers:
        headers = Template(headers).safe_substitute(dic_env)
    logger.info('-----------------------用例开始执行---------------------------')
    logger.info('-------------------------请求日志---------------------------')
    logger.info(f'用例编号：{case_id}')
    logger.info(f'用例标题：{title}')
    allure.attach(title, '用例标题')
    logger.info(f'请求方法：{method}')
    allure.attach(method, '请求方法')
    logger.info(f'请求地址：{url}')
    allure.attach(url, '请求地址')
    if headers:
        logger.info(f'请求头：{headers}')
        allure.attach(str(headers), '请求头', allure.attachment_type.TEXT)
    else:
        logger.info('当前测试用例的请求头为空')
    # 请求参数添加到allure报告
    if params:
        logger.info(f'请求参数：{params}')
        allure.attach(params, '请求参数', allure.attachment_type.TEXT)
    else:
        logger.info('当前测试用例的请求参数为空')
    dic_headers = None
    res = None
    if headers:
        dic_headers = json.loads(headers)
    if method.lower() == 'get' or method.lower() == 'delete':
        # 兼容get、delete请求参数params为空的情况
        if params:
            res = request(method, url, params=json.loads(params), headers=dic_headers)
        else:
            res = request(method, url, headers=dic_headers)
    elif method.lower() == 'post' or method.lower() == 'put':
        # 判断传参类型，如果Content-Type字段的值是application/json，表明是json传参
        if 'application/json' in dic_headers['Content-Type']:
            res = request(method, url, json=json.loads(params), headers=dic_headers)
        # 如果Content-Type字段的值是application/x-www-form-urlencoded，表明是form表单传参
        elif 'application/x-www-form-urlencoded' in dic_headers['Content-Type']:
            res = request(method, url, data=json.loads(params), headers=dic_headers)
        # 文件上传接口，通过headers指定的情况同时传递Content-Type和Authorization
        elif 'multipart/form-data' in dic_headers['Content-Type']:
            # 文件上传接口，通过headers指定的情况同时传递Content-Type和Authorization，指定了Content-Type之后
            # 默认把requests加的boundary字段的值进行覆盖，实际上传递给后端就没有boundary字段，最终会导致500的问题，去掉Content-Type
            dic_headers.pop('Content-Type')
            res = request(method, url, files=eval(params), headers=dic_headers)
    else:
        logger.error('当前请求方法不支持')
    logger.info('-------------------------响应日志---------------------------')
    logger.info(f'响应状态码：{res.status_code}')
    allure.attach(str(res.status_code), '响应状态码', allure.attachment_type.TEXT)
    logger.info(f'响应时间：{res.elapsed.total_seconds()}秒')
    allure.attach(str(res.elapsed.total_seconds()) + '秒', '响应时间', allure.attachment_type.TEXT)
    logger.info(f'响应头：{res.headers}')
    allure.attach(str(res.headers), '响应头', allure.attachment_type.TEXT)
    if res.text:
        logger.info(f'响应体：{res.text}')
        allure.attach(res.text, '响应体', allure.attachment_type.TEXT)
    else:
        logger.info('当前测试用例的响应体为空')
    return res


def assert_res(case, res):
    """
    统一响应断言封装
    :param case: 用例数据
    :param res: 接口响应
    :return: 没有返回
    """
    # 获取期望结果
    case_expect = case['期望结果']
    if case_expect:
        logger.info('-------------------------断言日志---------------------------')
        dic = json.loads(case_expect)
        # 遍历期望结果字典，k：响应字段，v：期望结果
        for k, v in dic.items():
            # 响应状态码断言
            if k == 'status_code':
                assert res.status_code == v
                logger.info(f'响应状态码断言，期望值：{v}，实际值：{res.status_code}')
            # 响应文本断言，完全相等
            elif k == 'text':
                assert res.text == v
                logger.info(f'响应体文本断言，期望值：{v}，实际值：{res.text}')
            # 响应字段断言，部分匹配
            elif k[0] == '$':
                # 提取JSONPath字段值
                jsonpath_result = jsonpath.jsonpath(res.json(), k)
                if not jsonpath_result:
                    logger.error(f"JSONPath表达式 {k} 未匹配到任何值")
                    assert False, f"JSONPath表达式 {k} 未匹配到任何值"

                actual_value = jsonpath_result[0]

                # 判断v是否为字典（嵌套断言条件）
                if isinstance(v, dict):
                    # 处理嵌套断言条件
                    for operator, expected_value in v.items():
                        if operator == '$ne':
                            # 不等于断言
                            assert actual_value != expected_value
                            logger.info(f'JSONPath断言，表达式：{k}，实际值：{actual_value} != {expected_value}（不等于断言）')
                        # 可以继续添加其他操作符，如$gt, $lt等
                else:
                    # 普通相等断言
                    assert actual_value == v
                    logger.info(f'JSONPath断言，表达式：{k}，期望值：{v}，实际值：{actual_value}')
    else:
        logger.info('当前用例未设置响应断言')

    # 将响应数据保存为xlsx文件
    # save_response_to_excel(case, res)


def save_response_to_excel(case, res):
    """
    将接口响应数据保存为xlsx表格文件（不依赖pandas）
    :param case: 用例数据
    :param res: 接口响应对象
    :return: None
    """
    try:
        # 确保AI_result文件夹存在
        result_dir = "AI_result"
        if not os.path.exists(result_dir):
            os.makedirs(result_dir)

        # 获取用例编号和标题用于文件命名
        case_id = case.get('用例编号', 'unknown')
        title = case.get('用例标题', 'unknown')

        # 构造文件名，确保包含.xlsx扩展名
        filename = f"{case_id}_{title}_response.xlsx"
        # 清理文件名中的非法字符
        filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-')).rstrip()
        # 确保文件名以.xlsx结尾
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        file_path = os.path.join(result_dir, filename)

        # 准备响应数据
        response_data = {
            "用例编号": case_id,
            "用例标题": title,
            "状态码": res.status_code,
            "响应时间(秒)": res.elapsed.total_seconds(),
            "响应体": res.text
        }

        # 如果响应体是JSON格式，将其展开
        try:
            json_data = res.json()
            if isinstance(json_data, dict):
                for key, value in json_data.items():
                    response_data[f"JSON_{key}"] = str(value)
            elif isinstance(json_data, list):
                response_data["JSON_数据"] = str(json_data)
        except Exception as e:
            logger.error(f"响应体不是有效的JSON格式，无法展开: {str(e)}")

        # 使用 openpyxl 写入 Excel
        wb = Workbook()
        ws = wb.active

        # 写入表头和数据
        headers = list(response_data.keys())
        values = list(response_data.values())
        ws.append(headers)  # 写入表头
        ws.append(values)  # 写入数据行

        # 保存文件
        wb.save(file_path)

        logger.info(f'响应数据已保存到: {file_path}')

    except Exception as e:
        logger.error(f'保存响应数据到Excel时出错: {str(e)}')


def assert_db(case):
    """
    数据库断言
    :param case: 用例数据
    :return: 没有返回
    """
    db_info = case['数据库断言']
    logger.info('-------------------------数据库断言---------------------------')
    if db_info:
        # 数据库断言，需要做参数替换
        db_dic = Template(db_info).safe_substitute(dic_env)
        dic = json.loads(db_dic)
        # k:代表执行的SQL语句，v:代表期望值
        for k, v in dic.items():
            # 执行SQL语句，获取结果
            result = query_db(k, option='one')[0]
            logger.info(f'数据库断言，期望值：{v}，实际值：{result}，执行的SQL语句：{k}')
            assert result == v
    else:
        logger.info('当前用例未设置数据库断言')
    logger.info('-------------------------用例执行结束---------------------------')


def extract_res(case, res):
    """
    提取响应字段
    :param case: 用例数据
    :param res: 响应结果
    :return: 没有返回
    """
    # 提取响应字段
    extract_info = case['提取响应字段']
    logger.info('-------------------------提取响应---------------------------')
    if extract_info:
        extract_dict = json.loads(extract_info)
        # for循环处理字典 {"token":"$..access_token","nickname":"$..nickname"}
        for k, v in extract_dict.items():
            # 两种情况：jsonpath提取响应字段的值、整个响应体文本数据提取
            if v == 'text':
                value = res.text
                logger.info(f'提取的字段：{k}，值：{value}')
            else:
                value = jsonpath.jsonpath(res.json(), v)[0]
                logger.info(f'提取的字段：{k}，值：{value}')
            # 关联字段的值需要保存到一个公共的数据容器中（可能会有多组，比如prod_id：116 sku_id：150 token：XXXX...）
            dic_env[k] = value
    else:
        logger.info('当前用例未设置提取响应字段')
