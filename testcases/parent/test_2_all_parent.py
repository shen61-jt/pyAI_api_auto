import allure
import pytest
from config.settings import IS_CI_ENV
from common.base_test import read_excel
from common.base_test import assert_res
from common.base_test import assert_db
from common.base_test import send_request
from common.base_test import extract_res
from common.base_test import dic_env
from config.settings import excel_path
from common.handle_data import get_unregister_phone
# from common.handle_data import get_unregister_username
# from common.handle_data import query_db

case_datas = read_excel(excel_path, '单接口验证')
# 提前构造生成满足要求的测试数据
phone = get_unregister_phone()
dic_env['mobile_phone'] = phone
# dic_env['user_name'] = get_unregister_username()


# allure报告中添加测试用例信息
@allure.epic('AI家长端项目')
@allure.feature('所有模块')
@allure.description("描述：所有测试模块")
@allure.link(url="https://minicourse.test.venhalo.com", name="接口地址")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.skipif(IS_CI_ENV, reason="在CI环境中跳过需要数据库连接的测试")
@pytest.mark.parametrize('case', case_datas)
def test_register(case):
    res = send_request(case)
    extract_res(case, res)
    assert_res(case, res)
    assert_db(case)
