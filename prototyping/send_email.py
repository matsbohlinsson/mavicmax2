import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

app_generated_password='saxxdxfygdcxhzaq'
my_address = "mats.bohlinsson@gmail.com"  # sender address
to_address= my_address

import smtplib
from email.message import EmailMessage

msg = MIMEMultipart()



msg["Subject"] = "The Email Subject"  # email subject
msg["From"] = my_address  # sender address
msg["To"] = to_address  # reciver address
msg.attach(MIMEText("Hello", 'plain'))
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(my_address, app_generated_password)  # login gmail account
    print("sending mail")

    file_path = "send_email.py"
    mimeBase = MIMEBase("application", "octet-stream")
    with open(file_path, "rb") as file:
        mimeBase.set_payload(file.read())
    encoders.encode_base64(mimeBase)
    mimeBase.add_header("Content-Disposition", f"attachment; filename={Path(file_path).name}")
    msg.attach(mimeBase)

    smtp.send_message(msg)  # send message
    print("mail has sent")


