import smtplib
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import smtplib



def send_email_with_attachments(subject: str, message:str, files:[Path], app_generated_password='saxxdxfygdcxhzaq', from_address ="mats.bohlinsson@gmail.com", to_address= None):
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = from_address  # sender address
    msg["To"] = to_address  # reciver address
    msg.attach(MIMEText(message, 'plain'))
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(from_address, app_generated_password)  # login gmail account

        for file in files:
            file_path = file.absolute()
            mimeBase = MIMEBase("application", "octet-stream")
            with open(file_path, "rb") as fileread:
                mimeBase.set_payload(fileread.read())
            encoders.encode_base64(mimeBase)
            mimeBase.add_header("Content-Disposition", f"attachment; filename={Path(file_path).name}")
            msg.attach(mimeBase)

        smtp.send_message(msg)  # send message
        print("mail has sent")

if __name__ == "__main__":
    p = Path('./inkommande_fakturor')
    files=[i for i in p.glob('*')]
    print(files)
    skip=True
    for i in files:
        if i.name=='12_google.pdf':skip=False
        if skip:
            print(f"skipping {i.name}")
            continue
        send_email_with_attachments(subject="subject",
                                message='Underlag Plain embedded',
                                files=[i],
                                app_generated_password = 'saxxdxfygdcxhzaq',
                                from_address="mats.bohlinsson@gmail.com",
                                to_address = "mats.bohlinsson@gmail.com")

        print(f"Sent:{[i]}")
        time.sleep(1)


