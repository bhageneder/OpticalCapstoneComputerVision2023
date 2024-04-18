import smtplib
from email.mime.text import MIMEText
import time
import subprocess
import board
import neopixel
import sys
import configparser

SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
SMTP_USERNAME = "opticalcomms23@yahoo.com"
SMTP_PASSWORD = "uqtjdtfqxtenmgtw"
EMAIL_FROM = "opticalcomms23@yahoo.com"

# Get robot name from config file
config = configparser.ConfigParser()
config.read("../src/config/config.cfg")
ROBOT = config['Name']['robotName']

def send_email(EMAIL_TO):
    output = subprocess.getoutput("ifconfig")
    co_msg = f"""
    {output}
    """
    EMAIL_SUBJECT = "IP ADDRESS RASPBERY PI " + ROBOT 
    msg = MIMEText(co_msg)
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = EMAIL_FROM 
    msg['To'] = EMAIL_TO

    debuglevel = True
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()

if __name__=='__main__':
    print('Sleeping for 45')
    time.sleep(45)
    # Capstone Group 2023
    #send_email("rgartrell@ycp.edu")
    #send_email("rblack5@ycp.edu")
    #send_email("kbeelitz1@ycp.edu")
    #send_email("jgilbert2@ycp.edu")
    # Capstone Group 2024
    send_email("mconrad4@ycp.edu")
    send_email("bhageneder@ycp.edu")
    send_email("mgeyer@ycp.edu")
    send_email("damao@ycp.edu")
    time.sleep(5)
    exit()