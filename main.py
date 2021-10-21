import sqlite3
import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import aiohttp
import asyncio


conn = sqlite3.connect(r'C:\....\contacts.db')
cursor = conn.cursor()

cursor.execute("SELECT first_name, last_name, email FROM contacts")
results = cursor.fetchall()

def parse_template(file_name):
    with open(file_name, 'r', encoding='utf-8') as msg_template:
        msg_template_content = msg_template.read()
        return Template(msg_template_content)

FROM_EMAIL = 'email@gmail.com'
MY_PASSWORD = 'password'


async def func(session, name_email):
    name_email = list(name_email)
    name = f'{name_email[0]} {name_email[1]}'
    email = f'{name_email[2]}'
    name_email = [name, email]
    return name_email


async def main():
    message_template = parse_template(r'C:\.....\message.txt')
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()
    smtp_server.login(FROM_EMAIL, MY_PASSWORD)
    async with aiohttp.ClientSession() as session:
        for name_email in results:
            name_email = await func(session, name_email)
            multipart_msg = MIMEMultipart()
            message = message_template.substitute(USER_NAME=name_email[0].title())
            print(message)
            try:
                multipart_msg['From'] = FROM_EMAIL
                multipart_msg['To'] = name_email[1]
                multipart_msg['Subject'] = "JournalDev Subject"
                multipart_msg.attach(MIMEText(message, 'plain'))
                smtp_server.send_message(multipart_msg)
            except Exception:
                print('')
            del multipart_msg

asyncio.run(main())

