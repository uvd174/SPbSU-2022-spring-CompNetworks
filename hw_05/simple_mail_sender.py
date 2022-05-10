#! /usr/local/bin/python
import sys
from email.mime.text import MIMEText
from smtplib import SMTP_SSL as SMTP


USERNAME = 'uvd2001@mail.ru'
PASSWORD = '60tt3VYR1b3R8ph56crT'

SMTP_server = 'smtp.mail.ru'
sender = 'uvd2001@mail.ru'

destination = sys.argv[1]

if sys.argv[2] not in {'txt', 'html'}:
    raise ValueError('Unsupported type of message!')
text_subtype = 'plain' if sys.argv[2] == 'txt' else sys.argv[2]

content_file_path = sys.argv[3]


with open(content_file_path, 'rt') as content_file:
    content = content_file.read()

subject = 'Sent from Python'


message = MIMEText(content, text_subtype)
message['Subject'] = subject
message['From'] = sender

with SMTP(SMTP_server) as connection:
    connection.set_debuglevel(False)
    connection.login(USERNAME, PASSWORD)
    connection.sendmail(sender, destination, message.as_string())
