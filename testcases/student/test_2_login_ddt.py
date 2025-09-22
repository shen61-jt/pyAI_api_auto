import allure
import pytest
from common.base_test import read_excel
from common.base_test import assert_res
from common.base_test import send_request
from config.settings import excel_path

# 按sheet读取Excel中的测试用例数据
case_datas = read_excel(excel_path, '登录')


@allure.epic('AI学生端项目')
@allure.feature('登录模块')
@allure.description("描述：登录模块")
@allure.link(url="http://shop.lemonban.com:8107/login", name="接口地址")
@allure.severity(allure.severity_level.BLOCKER)
# 从case_datas中逐条执行用例
@pytest.mark.parametrize('case', case_datas)
def test_login_ddt(case):
    res = send_request(case)
    assert_res(case, res)
