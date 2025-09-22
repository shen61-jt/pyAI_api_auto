import allure
import pytest
from common.base_test import read_excel
from common.base_test import assert_res
from common.base_test import assert_db
from common.base_test import send_request
from common.base_test import extract_res
from config.settings import excel_path

case_datas = read_excel(excel_path, '下单支付流程')


@allure.epic('AI学生端项目')
@allure.feature('订单模块')
@allure.description("描述：订单模块")
@allure.link(url="http://shop.lemonban.com:8107/login", name="接口地址")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize('case', case_datas)
def test_order(case):
    res = send_request(case)
    assert_res(case, res)
    extract_res(case, res)
    assert_db(case)
