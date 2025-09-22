import requests
from loguru import logger
from config.settings import WEIXIN


def send_weixin(content):
    """
    机器人向企业微信群推送测试结果
    @param content: 推送的内容
    @return:
    """
    url = f"{WEIXIN['url']}"
    headers = {"Content-Type": "application/json", "Charset": "UTF-8"}
    # @全体成员
    data = {"msgtype": "markdown","markdown": {"content": content, "mentioned_list": ["@all", ]}}
    res = requests.post(url=url, json=data, headers=headers)
    logger.info("发送企业微信测试结果成功！")
    return res.text
