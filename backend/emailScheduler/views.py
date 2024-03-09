import os
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.core.signals import request_finished
from django.dispatch import receiver
from django_crontab.crontab import Crontab

log_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'email.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def readHtmlFile(file_path):
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), file_path)
    with open(file_path, 'r') as file:
        html_content = file.read()
    return html_content

def sendMail():
    logging.info('Mail sending started...')
    try:
        sender_email = os.getenv('SENDER_EMAIL')
        receiver_email = os.getenv('RECEIVER_EMAIL')
        subject = "Hot things lost"
        html_file_path = "x.html"
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT'))
        smtp_username = os.getenv('SMTP_USERNAME')
        smtp_password = os.getenv('SMTP_PASSWORD')
        html_content = readHtmlFile(html_file_path)

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject
        message.attach(MIMEText(html_content, 'html'))
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password) 
            logging.info(smtp_username)
            server.sendmail(sender_email, receiver_email, message.as_string())
        
        logging.info('Mail sent successfully')
    except Exception as e:
        logging.error(e)


@receiver(request_finished)
def stop_cron_jobs(sender, **kwargs):
    # Stop all cron jobs
    Crontab().remove_all()
