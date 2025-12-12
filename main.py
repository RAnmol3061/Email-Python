import smtplib, sys, os

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from pathlib import Path

load_dotenv()

def read_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            file = f.read()
            return file
    except FileNotFoundError as e:
        print(f"Error: {e}")
        raise e
def read_file_text(file_path):
    try:
        with open(file_path, 'r') as f:
            file = f.read()
            return file
    except FileNotFoundError as e:
        print(f'Error: {e}')
        raise e
def read_file_html(file_path):
    try:
        with open(file_path, 'r') as f:
            file = f.read()
            return file
    except FileNotFoundError as e:
        print(f'Error: {e}')
        raise e
 
def email(plain_text, html_text, attachment_file, sender_email, receiver_email):
    
    mail = MIMEMultipart('mixed')
    mail["From"] = sender_email
    mail["To"] = receiver_email
    mail["Subject"] = "Subject of the Email"

    body = MIMEMultipart('alternative')
    email_body_plain = plain_text
    email_body_html = html_text

    body.attach(MIMEText(email_body_plain, "plain"))
    body.attach(MIMEText(email_body_html, "html"))

    attachment = MIMEApplication(read_file(attachment_file), _subtype='pdf')
    attachment.add_header('Content-Disposition','attachment',filename = attachment_file.name)
    attachment.add_header('Content-Transfer-Encoding', 'base64')

    mail.attach(body)
    mail.attach(attachment)

    return mail

host = os.getenv('host_name')
port = 587

login = os.getenv('login_email')
password = os.getenv('password')

sender_email = os.getenv('sender_email')
receiver_email = os.getenv('receiver_email')

file_path = "C.pdf"
p = Path(file_path)



text = Path("text.txt")
html = Path("html.txt")



try:
    with smtplib.SMTP(host,port) as server:
        server.starttls()
        server.login(login,password)
        server.sendmail(sender_email,receiver_email,email(read_file_text(text),read_file_html(html),p,sender_email,receiver_email).as_string())

except smtplib.SMTPAuthenticationError:
    print("Most probably the server didn’t accept the username/password combination provided.")   
except smtplib.SMTPRecipientsRefused:
    print(f"Recipient Refused: {smtplib.SMTP.sendmail()} ")
except smtplib.SMTPResponseException as e:
    print(f"{e.smtp_code}: {e.smtp_error}")
except Exception:
    print("Something wrong! Plz try again later")

else:
    print("Email was sent successfully")



