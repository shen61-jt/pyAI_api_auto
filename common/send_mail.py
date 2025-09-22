import yagmail
from loguru import logger
from config.settings import MAIL


def send_mail(attachments):
    """
    把测试报告作为附件发送到指定的QQ邮箱。
    """
    # user：发件人邮箱，password：发件人qq邮箱授权码，host：qq的服务器域名。
    mail_config = {"host": MAIL['host'],
                   "user": MAIL['send_user'],
                   "password": MAIL['password']
                   }
    yag = yagmail.SMTP(**mail_config)
    # 邮件标题。
    subject = "自动化测试报告"
    # 邮件内容。
    contents = "自动化测试结果推送，请查看附件内容。"
    # 收件人qq邮箱，设置to参数为list类型，可以给多个人发邮件。
    to = MAIL['receive_user']
    cc = MAIL['cc_user']
    bcc = MAIL['bcc_user']
    try:
        # 收件人邮箱和收件信息，设置send方法中的cc(抄送)和bcc(秘密抄送)参数，可添加抄送。当需要抄送或秘密抄送多个人时，cc/bcc参数设置为list。
        yag.send(to, subject, contents, attachments, cc, bcc)
        logger.info("邮件发送成功！")
        # 关闭服务。
        yag.close()
    except Exception as e:
        logger.error("邮件发送失败：{}".format(e))
