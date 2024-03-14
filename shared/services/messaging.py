import smtplib
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(email, totp_code):
    smtp_server = "smtp.laposte.net"
    smtp_port = 587
    sender_email = "arthur2klein@laposte.net"
    sender_password = base64.b64decode("R3NqbiZHYzJwJjJjcWRkbHA=").decode('utf-8')

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = email
    msg['Subject'] = "Double Authentification Code"

    # Add TOTP code to message body
    body = f"The code is: {totp_code}"
    msg.attach(MIMEText(body, 'plain'))
    print("Message created")

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        print("Starting server")
        server.starttls()
        print("Logging")
        server.login(sender_email, sender_password)
        print("Sending the message")
        server.send_message(msg)
