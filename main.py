import smtplib
import os

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv()

def read_file(file_path):
    try:
        with open(f"{file_path}", 'rb') as f:
            file = f.read()
            return file
    except Exception as e:
        print(f"Error {e}")

host = os.getenv('host_name')
port = 587

login = os.getenv('login_email')
password = os.getenv('password')

sender_email = os.getenv('sender_email')
receiver_email = os.getenv('receiver_email')

mail = MIMEMultipart('mixed')
mail["From"] = sender_email
mail["To"] = receiver_email
mail["Subject"] = "Subject of the Email"

body = MIMEMultipart('alternative')
email_body_plain = "Write something inside"
email_body_html = """\
<html>
    <body>
        <h1>Heading1</h1>
        <p>Lorem Ipsum</p>
        <h2>Heading2</h2>
        <p>Lorem Ipsum Lorem Ipsum</p>
    </body>
<html>
    """

body.attach(MIMEText(email_body_plain, "plain"))
body.attach(MIMEText(email_body_html, "html"))

attachment = MIMEApplication(read_file("C.pdf"), _subtype='pdf')
attachment.add_header('Content-Disposition','attachment',filename = "C.pdf")
attachment.add_header('Content-Transfer-Encoding', 'base64')

mail.attach(body)
mail.attach(attachment)

try:
    with smtplib.SMTP(host,port) as server:
        server.starttls()
        server.login(login,password)
        server.sendmail(sender_email,receiver_email,mail.as_string())

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