import os
import shutil
import sys
import time
import pytest
from loguru import logger
from common.send_mail import send_mail
from config.settings import log_path
from common.allure_reports import set_windows_title, get_json_data, write_json_data
from common.zip_files import zip_reports

# 移除默认的日志处理器
logger.remove()
# 通过日志文件记录接口运行信息（持久化存储），当日志文件大小达到10MB时，自动创建新文件继续记录，日志文件保留数量为10个
logger.add(sink=log_path, encoding="utf-8", level="INFO", rotation="10MB", retention=10)

# 控制台日志输出
logger.add(sys.stdout, level="INFO")

if __name__ == '__main__':
    pytest.main()
    # 复制environment.xml环境设置到allure报告
    shutil.copy('./environment.xml', './reports/temps')
    # 等待3s
    time.sleep(3)
    # 将report/temps文件夹下临时生成的json格式的测试报告，-o：输出到report/allures目录下生成index.html报告
    os.system(r"allure generate reports/temps -o reports/allures --clean")
    # 复制allure报告打开.bat文件到reports/allures下
    shutil.copy(r'reports/allure报告打开.bat', r'reports/allures')
    # 自定义allure报告网页标题
    set_windows_title("自动化测试报告标题")
    # 自定义allure报告标题
    report_title = get_json_data("自动化测试报告")
    write_json_data(report_title)
    # 调用方法，把reports/allures打包成zip文件到reports/report.zip
    zip_reports(r"reports/allures", r"reports/report.zip")
    # 报告的压缩包reports/report.zip
    report_path = os.path.join(r"reports", "report.zip")
    # 调用方法，发送报告的压缩包reports/report.zip测试报告到QQ邮箱
    send_mail(report_path)
    logger.info("接口自动化测试完成！")
    # 启动allure服务，自动打开报告
    # os.system(r'allure serve reports/temps')
