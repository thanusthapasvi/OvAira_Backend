import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv("c:/ovaira/.env")

sender_email = os.getenv("EMAIL_USER")
app_password = os.getenv("EMAIL_PASS")
receiver_email = "chaitanyaprakashkonisetty@gmail.com"

print(f"Sender: {sender_email}")
print(f"Receiver: {receiver_email}")

msg = MIMEText("This is a test email to verify delivery.")
msg["Subject"] = "Delivery Test"
msg["From"] = sender_email
msg["To"] = receiver_email

try:
    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.set_debuglevel(1)  # Enable debug output
    server.login(sender_email, app_password)
    print("Login successful. Sending mail...")
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Mail sent successfully!")
except Exception as e:
    print("Error:", e)
