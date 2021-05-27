import smtplib
from email.mime.text import MIMEText

from server import app, render_template
from settings import *


def sendMail(mail_to, data, template_name):
    subject = "Account Created"
    template = "mail_to_user.html"
    if template_name == "mail_to_user":
        template = "mail_to_user.html"
        subject = "Account Created"
    with app.app_context():
        html = render_template(template, data=data)
    msg = MIMEText(html, "html")
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = mail_to
    if MAIL_SEND:
        with smtplib.SMTP(MAIL_SMTP, MAIL_PORT) as server:
            server.starttls()
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(msg["From"], msg["To"], msg.as_string())
            print("mail successfully sent")
