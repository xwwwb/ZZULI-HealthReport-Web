import hashlib
import random
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def hash_code(s, salt='gdha4g456dsg25hs64g'):  # 加点盐
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())  # update方法只接收bytes类型
    return h.hexdigest()


def checkpassword(password):
    length = len(password)
    if length < 7:
        return 0
    else:
        return 1


def genrandom():
    strs = ""
    for i in range(6):
        ch = str(random.randrange(0, 9, 1))
        strs += ch
    return int(strs)

def sendcheckemail(my_user,checktext):
    my_sender="这里填发件邮箱"
    SMTPdomain="发件SMTP地址"
    SMTPauth="发件邮箱密码"
    msg = MIMEText("您正在找回密码，验证码为："+checktext,
                   'plain', 'utf-8')
    msg['From'] = formataddr(["轻工大健康打卡", my_sender])
    msg['To'] = formataddr(["找回密码", my_user])
    msg['Subject'] = "找回密码验证码"
    server = smtplib.SMTP_SSL(SMTPdomain, 465) # 这里端口改成和发件SMTP地址对应的
    server.login(my_sender, SMTPauth)
    server.sendmail(my_sender, [my_user, ], msg.as_string())
    server.quit()

