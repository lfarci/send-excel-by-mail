from smtplib import SMTP
from os import environ
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

smtp_hostname = environ.get('SMTP_HOSTNAME')
smtp_port = environ.get('SMTP_PORT')
sender_email = environ.get('SENDER_EMAIL')
sender_password = environ.get('SENDER_PASSWORD')
recipient_email = environ.get('RECIPIENT_EMAIL')

files = ["attachments/cat.jpg", "attachments/cat.pdf"]

print(f"Hostname: {smtp_hostname}")
print(f"Port: {smtp_port}")
print(f"Sender: {sender_email}")
print(f"Password: {sender_password is not None}")
print(f"Recipient: {recipient_email}")

s = SMTP(host = smtp_hostname, port = smtp_port)

s.ehlo()
s.starttls()
s.login(sender_email, sender_password)

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = recipient_email
msg['Date'] = formatdate(localtime=True)
msg['Subject'] = "Cats!"

msg.attach(MIMEText("Here's a sample mail with an attachment!"))

for f in files:
    with open(f, "rb") as fil:
        part = MIMEApplication(
            fil.read(),
            Name=basename(f)
        )
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
    msg.attach(part)

s.sendmail(sender_email, recipient_email, msg.as_string())

s.quit()