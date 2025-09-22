import time
import allure
import pytest
from common.base_test import read_excel
from common.base_test import assert_res
from common.base_test import extract_res
from common.base_test import send_request
from common.base_test import dic_env
from config.settings import excel_path
from common.handle_encrypt import rsa_str

case_datas = read_excel(excel_path, '充值项目测试')
# 构造timestamp及sign参数，并且保存到公共的数据容器中
timestamp = int(time.time())
dic_env['timestamp'] = timestamp


@allure.epic('AI学生端项目')
@allure.feature('充值模块')
@allure.description("描述：充值模块")
@allure.link(url="http://shop.lemonban.com:8107/login", name="接口地址")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize('case', case_datas)
def test_recharge(case):
    res = send_request(case)
    assert_res(case, res)
    # 该函数会提取对应的字段，并且保存到公共的数据容器中
    extract_res(case, res)
    # 等到登录接口调用完毕之后，再获取token生成sign签名
    if case['用例编号'] == 1:
        dic_env['sign'] = rsa_str(dic_env['token'][0:50] + str(timestamp))
