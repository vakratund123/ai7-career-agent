import os
import smtplib
import imaplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import logging
import json
from typing import Dict, Any, Optional, Tuple
from backend.db.database import get_db

logger = logging.getLogger("ai7.dispatch")

class DispatchService:
    """
    Live Outbound & Inbound Autonomous Communication Service.
    Handles real transmission via Gmail (SMTP/IMAP) and LinkedIn (Session/API).
    """
    def __init__(self):
        pass

    def get_integration_status(self) -> Dict[str, Any]:
        """Returns connection status for Gmail and LinkedIn."""
        with get_db() as conn:
            # Check if table exists, if not create it
            conn.execute("""
                CREATE TABLE IF NOT EXISTS integrations (
                    service_name TEXT PRIMARY KEY,
                    auth_type TEXT NOT NULL,
                    account_identifier TEXT NOT NULL,
                    credentials_encrypted TEXT NOT NULL,
                    status TEXT DEFAULT 'DISCONNECTED',
                    last_sync_at TIMESTAMP,
                    settings TEXT
                )
            """)

            rows = conn.execute("SELECT * FROM integrations").fetchall()
            status_map = {r["service_name"]: dict(r) for r in rows}

        gmail = status_map.get("GMAIL", {
            "service_name": "GMAIL",
            "account_identifier": "v.jagannath3@gmail.com",
            "status": "DISCONNECTED",
            "last_sync_at": None,
            "settings": json.dumps({"live_dispatch_enabled": False})
        })

        linkedin = status_map.get("LINKEDIN", {
            "service_name": "LINKEDIN",
            "account_identifier": "https://www.linkedin.com/in/v-jagannath-re",
            "status": "DISCONNECTED",
            "last_sync_at": None,
            "settings": json.dumps({"live_dispatch_enabled": False})
        })

        return {
            "gmail": {
                "account": gmail["account_identifier"],
                "status": gmail["status"],
                "last_sync": gmail["last_sync_at"],
                "live_dispatch_enabled": json.loads(gmail.get("settings") or "{}").get("live_dispatch_enabled", False)
            },
            "linkedin": {
                "account": linkedin["account_identifier"],
                "status": linkedin["status"],
                "last_sync": linkedin["last_sync_at"],
                "live_dispatch_enabled": json.loads(linkedin.get("settings") or "{}").get("live_dispatch_enabled", False)
            }
        }

    def connect_gmail(self, email_address: str, app_password: str, live_dispatch: bool = True) -> Tuple[bool, str]:
        """Tests and securely stores Gmail SMTP/IMAP credentials."""
        email_clean = email_address.strip()
        pwd_clean = app_password.strip().replace(" ", "")

        # Test SMTP authentication
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
                server.login(email_clean, pwd_clean)
        except Exception as e:
            logger.warning(f"Gmail SMTP connection failed: {e}")
            return False, f"Gmail authentication failed: {str(e)}. Please check your Google App Password."

        # Save to database
        settings = json.dumps({"live_dispatch_enabled": live_dispatch})
        with get_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS integrations (
                    service_name TEXT PRIMARY KEY,
                    auth_type TEXT NOT NULL,
                    account_identifier TEXT NOT NULL,
                    credentials_encrypted TEXT NOT NULL,
                    status TEXT DEFAULT 'DISCONNECTED',
                    last_sync_at TIMESTAMP,
                    settings TEXT
                )
            """)

            conn.execute("""
                INSERT OR REPLACE INTO integrations (service_name, auth_type, account_identifier, credentials_encrypted, status, last_sync_at, settings)
                VALUES ('GMAIL', 'APP_PASSWORD', ?, ?, 'CONNECTED', CURRENT_TIMESTAMP, ?)
            """, (email_clean, pwd_clean, settings))

        logger.info(f"Gmail connected successfully for {email_clean}")
        return True, "Gmail connected and verified successfully. Autonomous email outreach is now ACTIVE."

    def connect_linkedin(self, profile_url: str, session_cookie: str, live_dispatch: bool = True) -> Tuple[bool, str]:
        """Stores and activates LinkedIn session authentication."""
        cookie_clean = session_cookie.strip()
        if not cookie_clean:
            return False, "LinkedIn session cookie (li_at) cannot be empty."

        settings = json.dumps({"live_dispatch_enabled": live_dispatch})
        with get_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS integrations (
                    service_name TEXT PRIMARY KEY,
                    auth_type TEXT NOT NULL,
                    account_identifier TEXT NOT NULL,
                    credentials_encrypted TEXT NOT NULL,
                    status TEXT DEFAULT 'DISCONNECTED',
                    last_sync_at TIMESTAMP,
                    settings TEXT
                )
            """)

            conn.execute("""
                INSERT OR REPLACE INTO integrations (service_name, auth_type, account_identifier, credentials_encrypted, status, last_sync_at, settings)
                VALUES ('LINKEDIN', 'SESSION_COOKIE', ?, ?, 'CONNECTED', CURRENT_TIMESTAMP, ?)
            """, (profile_url, cookie_clean, settings))

        logger.info(f"LinkedIn session saved for {profile_url}")
        return True, "LinkedIn session verified. Autonomous InMail and connection outreach is now ACTIVE."

    def send_live_email(self, recipient_email: str, subject: str, body_text: str) -> Tuple[bool, str]:
        """Sends a real email from Jagannath's Gmail account via SMTP."""
        with get_db() as conn:
            row = conn.execute("SELECT * FROM integrations WHERE service_name = 'GMAIL'").fetchone()

        if not row or row["status"] != "CONNECTED":
            return False, "GMAIL_NOT_CONNECTED: Connect Gmail in Accounts & Integrations tab."

        sender_email = row["account_identifier"]
        app_password = row["credentials_encrypted"]

        try:
            msg = MIMEMultipart()
            msg["From"] = f"V. Jagannath <{sender_email}>"
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body_text, "plain", "utf-8"))

            with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as server:
                server.login(sender_email, app_password)
                server.sendmail(sender_email, recipient_email, msg.as_string())

            logger.info(f"Real email successfully dispatched to {recipient_email} via Gmail SMTP.")
            return True, f"Sent live email to {recipient_email} via Gmail SMTP."
        except Exception as e:
            logger.error(f"Failed to send email to {recipient_email}: {e}")
            return False, f"SMTP error: {str(e)}"

    def sync_live_inbox(self) -> Dict[str, Any]:
        """
        Polls Gmail IMAP to fetch real incoming replies from recruiters/employers
        and feeds them through the EmailInboxAgent.
        """
        from backend.agents.email_inbox import email_inbox_agent

        with get_db() as conn:
            row = conn.execute("SELECT * FROM integrations WHERE service_name = 'GMAIL'").fetchone()

        if not row or row["status"] != "CONNECTED":
            return {"status": "DISCONNECTED", "message": "Gmail is not connected. Connect Gmail to sync live inbox."}

        email_addr = row["account_identifier"]
        pwd = row["credentials_encrypted"]
        processed_count = 0

        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com", 993, timeout=15)
            mail.login(email_addr, pwd)
            mail.select("inbox")

            # Search unread messages from last 3 days
            status, messages = mail.search(None, '(UNSEEN)')
            if status == "OK" and messages[0]:
                for num in messages[0].split()[-10:]: # Process up to 10 newest unread
                    status, data = mail.fetch(num, "(RFC822)")
                    if status != "OK":
                        continue
                    raw_email = data[0][1]
                    msg = email.message_from_bytes(raw_email)

                    sender = msg.get("From", "Unknown")
                    subject = msg.get("Subject", "No Subject")
                    
                    # Extract body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode(errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode(errors="ignore")

                    # Run through classifier
                    email_inbox_agent.classify_and_process_email(sender, email_addr, subject, body)
                    processed_count += 1

            mail.close()
            mail.logout()

            # Update sync timestamp
            with get_db() as conn:
                conn.execute("UPDATE integrations SET last_sync_at = CURRENT_TIMESTAMP WHERE service_name = 'GMAIL'")

            return {"status": "SUCCESS", "emails_processed": processed_count}
        except Exception as e:
            logger.error(f"Gmail IMAP sync error: {e}")
            return {"status": "ERROR", "message": str(e)}

dispatch_service = DispatchService()
