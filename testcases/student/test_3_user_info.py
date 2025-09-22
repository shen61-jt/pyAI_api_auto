import allure
import pytest
from common.base_test import read_excel
from common.base_test import assert_res
from common.base_test import send_request
from common.base_test import extract_res
from config.settings import excel_path

case_datas = read_excel(excel_path, '修改用户头像流程')


@allure.epic('AI学生端项目')
@allure.feature('用户模块')
@allure.description("描述：用户模块")
@allure.link(url="http://shop.lemonban.com:8107/p/user/setUserInfo", name="接口地址")
@allure.severity(allure.severity_level.BLOCKER)
@pytest.mark.parametrize('case', case_datas)
def test_modify_user(case):
    res = send_request(case)
    extract_res(case, res)
    assert_res(case, res)
