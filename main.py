import smtplib
import os
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

host = os.getenv('host_name')
port = os.getenv('port_value', 587)

login = os.getenv('login_email')
password = os.getenv('password')

sender_email = os.getenv('sender_email')
receiver_email = os.getenv('receiver_email')

text = "Why is it so difficult"

message = MIMEMultipart('alternative')
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "Welcome to Mailtrap"


html_content = """\
<html>
    <body>
        <h1>FRIDGE ME Welcome to Mailtrap</h1>
        <p>Why is it so difficult</p>
        <h2>Heck me</h2>
    </body>
<html>
    """

message.attach(MIMEText((text), "plain"))
message.attach(MIMEText(html_content, "html"))
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

print("Done")