import yagmail
from loguru import logger
from config.settings import MAIL
import time


def send_mail(attachments):
    """
    把测试报告作为附件发送到指定的QQ邮箱。
    """
    mail_config = {
        "host": MAIL['host'],
        'port': 465,
        "user": MAIL['send_user'],
        "password": MAIL['password']
    }

    max_retries = 3
    for attempt in range(max_retries):
        try:
            # 添加连接超时设置
            yag = yagmail.SMTP(**mail_config, smtp_ssl=True)

            subject = "自动化测试报告"
            contents = "自动化测试结果推送，请查看附件内容。"
            to = MAIL['receive_user']
            cc = MAIL['cc_user']
            bcc = MAIL['bcc_user']

            yag.send(to, subject, contents, attachments, cc, bcc)
            logger.info("邮件发送成功！")
            yag.close()
            break

        except Exception as e:
            logger.error(f"邮件发送失败（尝试{attempt + 1}/{max_retries}）：{str(e)}")
            if attempt < max_retries - 1:
                time.sleep(5)  # 等待5秒后重试
            else:
                logger.error("邮件发送最终失败")
