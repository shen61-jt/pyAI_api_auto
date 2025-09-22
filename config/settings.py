from pathlib import Path

# excel文件的路径
excel_path = Path(__file__).parent.parent / 'datas' / 'data.xlsx'
# 日志文件的路径
log_path = Path(__file__).parent.parent / 'logs' / 'api_auto.log'

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
    'secret': 'SECdfb951a25ae2485648320d82a83e64095916556f0e4e2ab03e268f919c9177a1',
    'url': 'https://oapi.dingtalk.com/robot/send?access_token=f8438068a6a6e4c98f6476b90340357fa6aafd32d93e70c67112dd8c5bd9c5d7'
}

# # 企业微信通知配置
# WEIXIN = {
#     'url': 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=1ed59978-7084-411c-abba-32eb1b13b2d7'
# }

# QQ邮箱配置
MAIL = {
    'host': 'smtp.qq.com',
    'send_user': '527005944@qq.com',
    'password': '',
    'receive_user': '527005944@qq.com',
    'cc_user': None,
    'bcc_user': None
}
