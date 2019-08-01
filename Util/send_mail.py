import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from ProjVar.var import *

import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

def send_mail():
    mail_host="smtp.163.com"  #设置服务器
    mail_user="15001241323"    #用户名
    mail_pass="Whk3sfvp69"   #口令
    sender = '15001241323@163.com'
    receivers = ['110674363@qq.com',"35543638@qq.com"] # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # 创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = formataddr(["光荣之路", "15001241323@163.com"])
    message['To'] = ','.join(receivers)
    subject = '自动化测试执行报告'
    message['Subject'] = Header(subject, 'utf-8')
    message["Accept-Language"]="zh-CN"
    message["Accept-Charset"]="ISO-8859-1,utf-8,gbk"
    # 邮件正文内容
    message.attach(MIMEText('最新执行的自动化测试报告，请参阅附件内容！', 'plain', 'utf-8'))

    # 构造附件1，传送测试结果的excel文件
    att = MIMEBase('application', 'octet-stream')
    att.set_payload(open(ProjDirPath+"\\testdata\\data.xlsx", 'rb').read())
    att.add_header('Content-Disposition', 'attachment', filename=('gbk', '', "自动化测试报告.xlsx"))
    encoders.encode_base64(att)
    message.attach(att)
    """
    # 构造附件2，传送当前目录下的 runoob.txt 文件
    att2 = MIMEText(open('e:\\a.py','rb').read(), 'base64', 'utf-8')
    att2["Content-Type"] = 'application/octet-stream'
    att2["Content-Disposition"] = 'attachment; filename="a.py"'
    message.attach(att2)
    """
    try:
        smtpObj = smtplib.SMTP(mail_host)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException as e:
        print("Error: 无法发送邮件", e)

if __name__ == "__main__":
    send_mail()