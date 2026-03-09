import smtplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from fastapi import BackgroundTasks
from database import get_db_connection
from utils import generate_otp, generate_session_token

def send_otp_email(background_tasks: BackgroundTasks, email: str, otp: str):
    """Queue email sending as a background task."""
    background_tasks.add_task(_send_email, email, otp)

def _send_email(to_email: str, otp: str):
    """Actual SMTP send function (runs in background)."""
    smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")   # default Gmail
    smtp_port = int(os.getenv("EMAIL_PORT", 587))           # default TLS port
    smtp_user = os.getenv("EMAIL_USER")                     # your email address
    smtp_pass = os.getenv("EMAIL_PASSWORD")                 # app password
    from_email = os.getenv("EMAIL_FROM", smtp_user)

    subject = "Your OTP for Smart File Organizer"
    body = f"Your OTP is: {otp}\nIt is valid for 10 minutes."

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
        print(f"✅ OTP email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

def store_otp(email: str, otp: str):
    """Store OTP and expiry in the database (10 minutes validity)."""
    expiry = time.time() + 600  # 10 minutes
    conn = get_db_connection()
    cursor = conn.cursor()
    # Upsert: insert or replace
    cursor.execute("""
        INSERT OR REPLACE INTO users (email, otp_code, otp_expiry, session_token)
        VALUES (?, ?, ?, NULL)
    """, (email, otp, expiry))
    conn.commit()
    conn.close()

def verify_otp(email: str, otp: str):
    """Check if OTP is valid and not expired. If valid, generate session token."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT otp_code, otp_expiry FROM users WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None

    stored_otp = row["otp_code"]
    expiry = row["otp_expiry"]

    if stored_otp != otp or time.time() > expiry:
        conn.close()
        return None

    # OTP valid, generate session token
    token = generate_session_token()
    cursor.execute("UPDATE users SET session_token = ? WHERE email = ?", (token, email))
    conn.commit()
    conn.close()
    return token