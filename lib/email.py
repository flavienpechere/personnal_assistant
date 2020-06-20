import smtplib
from email.message import EmailMessage
from getpass import getpass
from smtplib import SMTP_SSL
import webbrowser

def new_email(subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = from_email_address
    msg['To'] = to_email_address
    
    return msg
    
def send_email(msg, password):
    #password = getpass(password)
    s = smtplib.SMTP('smtp.gmail.com', 587, timeout=10)
    s.set_debuglevel(1)
    s.starttls()
    s.ehlo()
    s.login(msg['From'], password)
    s.send_message(msg)
    s.quit()
    
def new_mailto(subject, body):
    webbrowser.open('mailto:?to=' + '&subject=' + subject + '&body=' + body, new=1)