import os
from pathlib import Path

# excel文件的路径
excel_path = Path(__file__).parent.parent / 'datas' / 'data.xlsx'
# 日志文件的路径
log_path = Path(__file__).parent.parent / 'logs' / 'api_auto.log'
# 检查是否在CI环境中
IS_CI_ENV = os.environ.get('CI', '').lower() == 'true' or os.environ.get('GITHUB_ACTIONS', '').lower() == 'true'

# 数据库的配置信息
MQ_CONFIG = {
    'host': 'rm-2vc9sj517iz7642px1o.mysql.cn-chengdu.rds.aliyuncs.com',
    'port': 3306,
    'username': 'root',
    'password': 'Wanglinan@!@#$%^',
    'database': 'minicourse_test',
    'charset': 'utf8'
}

# # jenkins配置
# JENKINS = {
#     'url': 'http://127.0.0.1:8080/jenkins/',
#     'username': 'peiyu',
#     'password': '123456',
#     'timeout': 30,
#     'job_name': 'py69_api_auto'
# }

# 项目名
project_name = 'pyAI_api_auto'

# # 钉钉通知配置
DINGDING = {
    'secret': 'SEC5ba3a6f2dae7cdc1529af0ecbbe420f480b020c917caa23817387e32bbe095b6',
    'url': 'https://oapi.dingtalk.com/robot/send?access_token=fc46690c1c360a53ee53b3c1b9995027fcb18efefc891692f5824df7ba801fe7'
}

# # 企业微信通知配置
# WEIXIN = {
#     'url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1ed59978-7084-411c-abba-32eb1b13b2d7'
# }

# QQ邮箱配置
MAIL = {
    'host': 'smtp.qq.com',
    'send_user': '527005944@qq.com',
    'password': 'dqmtjasisbnbbgbc',
    'receive_user': '527005944@qq.com',
    'cc_user': '2879205362@qq.com',
    'bcc_user': None
}

import os
from pathlib import Path

# excel文件的路径
excel_path = Path(__file__).parent.parent / 'datas' / 'data.xlsx'
# 日志文件的路径
log_path = Path(__file__).parent.parent / 'logs' / 'api_auto.log'
# 检查是否在CI环境中
IS_CI_ENV = os.environ.get('CI', '').lower() == 'true' or os.environ.get('GITHUB_ACTIONS', '').lower() == 'true'

