import smtplib, os
import tkinter as tk

from dotenv import load_dotenv
from tkinter import filedialog

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

sender_email = os.getenv('sender_email')
receiver_email = os.getenv('receiver_email')

def email(plain_text, html_text, attachment_file):
    
    mail = MIMEMultipart('mixed')
    mail["From"] = sender_email
    mail["To"] = receiver_email
    mail["Subject"] = "Subject of the Email"

    body = MIMEMultipart('alternative')

    body.attach(MIMEText(plain_text, "plain"))
    body.attach(MIMEText(html_text, "html"))

    attachment = MIMEApplication(read_file(attachment_file), _subtype='pdf')
    attachment.add_header('Content-Disposition','attachment',filename = attachment_file.name)
    attachment.add_header('Content-Transfer-Encoding', 'base64')

    mail.attach(body)
    mail.attach(attachment)

    return mail

def open_filedialog():
    root = tk.Tk()
    root.withdraw()

    filepath = filedialog.askopenfilename(
        title = 'Select a file to upload',
        initialdir = os.getcwd(),
        filetypes = [("All files","*.*"),("PDF files","*.pdf*"),("Text file","*.txt*")]
    )

    if filepath:
        return filepath
    else:
        return(None)

file_path_attachment = Path(open_filedialog())
text = Path(open_filedialog())
html = Path(open_filedialog())


def connection(login,password):
    host = os.getenv('host_name')
    port = 587

    try:
        with smtplib.SMTP(host,port) as server:
            server.starttls()
            server.login(login,password)
            server.sendmail(sender_email,receiver_email,email(read_file_text(text),read_file_html(html),file_path_attachment).as_string())

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

connection(os.getenv('login_email'),os.getenv('password'))
