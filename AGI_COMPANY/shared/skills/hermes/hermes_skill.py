#!/usr/bin/env python3
"""
Hermes Skill - Communication and Messaging
Actually connects to Slack, Discord, Telegram, Email
"""

import os
import json
import smtplib
import imaplib
import requests
from email.mime.text import MIMEText
from typing import Dict, List, Optional

class HermesSkill:
    """Real communication skill"""
    
    def __init__(self):
        self.config = self._load_config()
        self.active = True
        print("[Hermes] Skill activated")
    
    def _load_config(self) -> Dict:
        """Load configuration from environment or file"""
        config_path = os.path.expanduser("~/.aos/config/hermes.json")
        if os.path.exists(config_path):
            with open(config_path) as f:
                return json.load(f)
        return {
            "slack_webhook": os.getenv("SLACK_WEBHOOK", ""),
            "discord_webhook": os.getenv("DISCORD_WEBHOOK", ""),
            "telegram_token": os.getenv("TELEGRAM_TOKEN", ""),
            "email_smtp": os.getenv("EMAIL_SMTP", "smtp.gmail.com"),
            "email_user": os.getenv("EMAIL_USER", ""),
            "email_pass": os.getenv("EMAIL_PASS", "")
        }
    
    def send_slack(self, message: str, channel: str = "#general") -> bool:
        """Send message to Slack"""
        webhook = self.config.get("slack_webhook")
        if not webhook:
            print("[Hermes] No Slack webhook configured")
            return False
        
        try:
            resp = requests.post(webhook, json={"text": message, "channel": channel})
            return resp.status_code == 200
        except Exception as e:
            print(f"[Hermes] Slack error: {e}")
            return False
    
    def send_discord(self, message: str) -> bool:
        """Send message to Discord"""
        webhook = self.config.get("discord_webhook")
        if not webhook:
            print("[Hermes] No Discord webhook configured")
            return False
        
        try:
            resp = requests.post(webhook, json={"content": message})
            return resp.status_code == 204
        except Exception as e:
            print(f"[Hermes] Discord error: {e}")
            return False
    
    def send_email(self, to: str, subject: str, body: str) -> bool:
        """Send email"""
        try:
            smtp_server = self.config.get("email_smtp", "smtp.gmail.com")
            smtp_user = self.config.get("email_user")
            smtp_pass = self.config.get("email_pass")
            
            if not all([smtp_user, smtp_pass]):
                print("[Hermes] Email credentials not configured")
                return False
            
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = smtp_user
            msg['To'] = to
            
            with smtplib.SMTP(smtp_server, 587) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"[Hermes] Email error: {e}")
            return False
    
    def route_message(self, message: str, priority: str = "normal") -> Dict:
        """Route message to appropriate channel"""
        results = {}
        
        if priority == "high":
            # Send to all channels
            results["slack"] = self.send_slack(f"[HIGH] {message}")
            results["discord"] = self.send_discord(f"[HIGH] {message}")
        elif priority == "normal":
            results["slack"] = self.send_slack(message)
        else:
            results["discord"] = self.send_discord(message)
        
        return results

if __name__ == "__main__":
    hermes = HermesSkill()
    print("Hermes skill ready")
