import smtplib
import os

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

host = os.getenv('host_name')
port = 587

login = os.getenv('login_email')
password = os.getenv('password')

sender_email = os.getenv('sender_email')
receiver_email = os.getenv('receiver_email')

email_body_plain = "Write something inside"

message = MIMEMultipart('alternative')
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Subject of the Email"


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

message.attach(MIMEText(email_body_plain, "plain"))
message.attach(MIMEText(email_body_html, "html"))


try:
    with smtplib.SMTP(host,port) as server:
        server.starttls()
        server.login(login,password)
        server.sendmail(sender_email,receiver_email,message.as_string())

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