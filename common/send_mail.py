# 在 common/send_mail.py 中修改 send_mail 函数
import traceback
import yagmail
from loguru import logger
from config.settings import MAIL


def send_mail(attachments):
    """
    把测试报告作为附件发送到指定的QQ邮箱。
    """
    # user：发件人邮箱，password：发件人qq邮箱授权码，host：qq的服务器域名。
    mail_config = {"host": MAIL['host'],
                   'port': 465,  # 确认端口号(587/465/25)
                   "user": MAIL['send_user'],
                   "password": MAIL['password']
                   }

    try:
        yag = yagmail.SMTP(**mail_config)
        # 邮件标题。
        subject = "自动化测试报告"
        # 邮件内容。
        contents = "自动化测试结果推送，请查看附件内容。"
        # 收件人qq邮箱，设置to参数为list类型，可以给多个人发邮件。
        to = MAIL['receive_user']
        cc = MAIL['cc_user']
        bcc = MAIL['bcc_user']

        # 记录发送前的配置信息（敏感信息打码）
        logger.info(f"准备发送邮件 - SMTP服务器: {MAIL['host']}:{465}")
        logger.info(f"发件人: {MAIL['send_user']}")
        logger.info(f"收件人数量: {len(to) if isinstance(to, list) else 1}")

        # 收件人邮箱和收件信息，设置send方法中的cc(抄送)和bcc(秘密抄送)参数，可添加抄送。当需要抄送或秘密抄送多个人时，cc/bcc参数设置为list。
        yag.send(to, subject, contents, attachments, cc, bcc)
        logger.info("邮件发送成功！")
        # 关闭服务。
        yag.close()
    except Exception as e:
        # 记录详细的错误信息和堆栈跟踪
        error_msg = f"邮件发送失败：{str(e)}"
        logger.error(error_msg)
        logger.error(f"错误类型: {type(e).__name__}")
        logger.error(f"详细堆栈信息:\n{traceback.format_exc()}")

        # 记录邮件配置信息用于排查（敏感信息打码）
        logger.info(f"邮件配置检查 - Host: {MAIL['host']}, Port: {465}")
        logger.info(f"发件人邮箱: {MAIL['send_user']}")
        logger.info(f"收件人邮箱: {MAIL['receive_user']}")

        # 确保连接关闭
        try:
            yag.close()
        except:
            pass
