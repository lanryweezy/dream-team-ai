"""
Email Manager
Handles email campaigns, automation, and analytics
"""

import os
import json
import logging
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import time

logger = logging.getLogger(__name__)

class EmailManager:
    def __init__(self, 
                 provider: str = "smtp",
                 api_key: Optional[str] = None,
                 smtp_config: Optional[Dict[str, Any]] = None):
        self.provider = provider.lower()
        self.api_key = api_key
        self.smtp_config = smtp_config or {}
        
        # Provider configurations
        self.providers = {
            "sendgrid": {
                "api_url": "https://api.sendgrid.com/v3/mail/send",
                "headers": {
                    "Authorization": f"Bearer {api_key or ''}",
                    "Content-Type": "application/json"
                }
            },
            "mailgun": {
                "api_url": "https://api.mailgun.net/v3",
                "auth": ("api", api_key or "")
            },
            "smtp": {
                "server": self.smtp_config.get("server", "smtp.gmail.com") if self.smtp_config else "smtp.gmail.com",
                "port": self.smtp_config.get("port", 587) if self.smtp_config else 587,
                "username": self.smtp_config.get("username", "") if self.smtp_config else "",
                "password": self.smtp_config.get("password", "") if self.smtp_config else ""
            }
        }
        
    def send_email(self, 
                   to_email: str,
                   subject: str,
                   content: str,
                   from_email: Optional[str] = None,
                   from_name: Optional[str] = None,
                   html_content: Optional[str] = None,
                   attachments: Optional[List[str]] = None) -> Dict[str, Any]:
        """Send a single email"""
        
        try:
            if self.provider == "sendgrid":
                return self._send_via_sendgrid(to_email, subject, content, from_email or "", from_name or "", html_content or "")
            elif self.provider == "mailgun":
                return self._send_via_mailgun(to_email, subject, content, from_email or "", from_name or "", html_content or "")
            elif self.provider == "smtp":
                return self._send_via_smtp(to_email, subject, content, from_email or "", from_name or "", html_content or "", attachments or [])
            else:
                return {
                    "success": False,
                    "error": f"Provider '{self.provider}' not supported"
                }
                
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def send_bulk_email(self, 
                       recipients: List[Dict[str, str]],
                       subject: str,
                       content: str,
                       from_email: Optional[str] = None,
                       from_name: Optional[str] = None,
                       html_content: Optional[str] = None,
                       batch_size: int = 100,
                       delay: float = 1.0) -> Dict[str, Any]:
        """Send bulk emails with rate limiting"""
        
        try:
            results = []
            total_recipients = len(recipients)
            
            # Process in batches
            for i in range(0, total_recipients, batch_size):
                batch = recipients[i:i + batch_size]
                batch_results = []
                
                for recipient in batch:
                    # Personalize content if needed
                    personalized_content = self._personalize_content(content, recipient)
                    personalized_html = self._personalize_content(html_content, recipient) if html_content else None
                    
                    result = self.send_email(
                        to_email=recipient["email"],
                        subject=subject,
                        content=personalized_content,
                        from_email=from_email,
                        from_name=from_name,
                        html_content=personalized_html
                    )
                    
                    batch_results.append({
                        "email": recipient["email"],
                        "success": result["success"],
                        "error": result.get("error")
                    })
                    
                    # Rate limiting
                    if delay > 0:
                        time.sleep(delay)
                        
                results.extend(batch_results)
                
                # Log progress
                logger.info(f"Processed batch {i//batch_size + 1}/{(total_recipients-1)//batch_size + 1}")
                
            # Calculate statistics
            successful = sum(1 for r in results if r["success"])
            failed = total_recipients - successful
            
            return {
                "success": True,
                "total_sent": total_recipients,
                "successful": successful,
                "failed": failed,
                "results": results
            }
            
        except Exception as e:
            logger.error(f"Failed to send bulk email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def create_email_campaign(self, 
                             campaign_name: str,
                             subject: str,
                             content: str,
                             html_content: Optional[str] = None,
                             recipients: Optional[List[Dict[str, str]]] = None,
                             schedule_time: Optional[datetime] = None) -> Dict[str, Any]:
        """Create an email campaign"""
        
        try:
            campaign = {
                "id": f"campaign_{int(time.time())}",
                "name": campaign_name,
                "subject": subject,
                "content": content,
                "html_content": html_content,
                "recipients": recipients or [],
                "created_at": datetime.now().isoformat(),
                "schedule_time": schedule_time.isoformat() if schedule_time else None,
                "status": "draft",
                "stats": {
                    "sent": 0,
                    "delivered": 0,
                    "opened": 0,
                    "clicked": 0,
                    "bounced": 0,
                    "unsubscribed": 0
                }
            }
            
            # Save campaign
            self._save_campaign(campaign)
            
            return {
                "success": True,
                "campaign_id": campaign["id"],
                "campaign": campaign
            }
            
        except Exception as e:
            logger.error(f"Failed to create campaign: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def send_campaign(self, campaign_id: str) -> Dict[str, Any]:
        """Send an email campaign"""
        
        try:
            campaign = self._load_campaign(campaign_id)
            if not campaign:
                return {
                    "success": False,
                    "error": "Campaign not found"
                }
                
            # Check if scheduled
            if campaign.get("schedule_time"):
                schedule_time = datetime.fromisoformat(campaign["schedule_time"])
                if datetime.now() < schedule_time:
                    return {
                        "success": False,
                        "error": f"Campaign scheduled for {schedule_time}"
                    }
                    
            # Send bulk email
            result = self.send_bulk_email(
                recipients=campaign["recipients"],
                subject=campaign["subject"],
                content=campaign["content"],
                html_content=campaign.get("html_content")
            )
            
            # Update campaign status
            campaign["status"] = "sent" if result["success"] else "failed"
            campaign["sent_at"] = datetime.now().isoformat()
            campaign["stats"]["sent"] = result.get("successful", 0)
            
            self._save_campaign(campaign)
            
            return {
                "success": result["success"],
                "campaign_id": campaign_id,
                "stats": result
            }
            
        except Exception as e:
            logger.error(f"Failed to send campaign: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def create_email_sequence(self, 
                             sequence_name: str,
                             emails: List[Dict[str, Any]],
                             trigger_event: str = "signup") -> Dict[str, Any]:
        """Create an automated email sequence"""
        
        try:
            sequence = {
                "id": f"sequence_{int(time.time())}",
                "name": sequence_name,
                "trigger_event": trigger_event,
                "emails": emails,
                "created_at": datetime.now().isoformat(),
                "active": True,
                "stats": {
                    "triggered": 0,
                    "completed": 0,
                    "conversion_rate": 0
                }
            }
            
            # Validate email sequence
            for i, email in enumerate(emails):
                if not all(key in email for key in ["subject", "content", "delay_days"]):
                    return {
                        "success": False,
                        "error": f"Email {i+1} missing required fields"
                    }
                    
            # Save sequence
            self._save_sequence(sequence)
            
            return {
                "success": True,
                "sequence_id": sequence["id"],
                "sequence": sequence
            }
            
        except Exception as e:
            logger.error(f"Failed to create sequence: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def trigger_sequence(self, 
                        sequence_id: str,
                        recipient_email: str,
                        recipient_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Trigger an email sequence for a recipient"""
        
        try:
            sequence = self._load_sequence(sequence_id)
            if not sequence:
                return {
                    "success": False,
                    "error": "Sequence not found"
                }
                
            if not sequence.get("active"):
                return {
                    "success": False,
                    "error": "Sequence is not active"
                }
                
            # Create sequence instance
            instance = {
                "id": f"instance_{int(time.time())}_{recipient_email.replace('@', '_')}",
                "sequence_id": sequence_id,
                "recipient_email": recipient_email,
                "recipient_data": recipient_data or {},
                "started_at": datetime.now().isoformat(),
                "current_step": 0,
                "completed": False,
                "emails_sent": []
            }
            
            # Save instance
            self._save_sequence_instance(instance)
            
            # Send first email immediately if delay is 0
            if sequence["emails"][0].get("delay_days", 0) == 0:
                self._send_sequence_email(instance, 0)
                
            return {
                "success": True,
                "instance_id": instance["id"],
                "message": "Sequence triggered successfully"
            }
            
        except Exception as e:
            logger.error(f"Failed to trigger sequence: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def create_waitlist_email(self, 
                             company_name: str,
                             product_name: str,
                             launch_date: Optional[str] = None) -> Dict[str, Any]:
        """Create a waitlist confirmation email"""
        
        try:
            subject = f"Welcome to the {product_name} waitlist!"
            
            content = f"""Hi there!

Thank you for joining the {product_name} waitlist. We're thrilled to have you on board!

{company_name} is working hard to bring you an amazing product that will revolutionize your workflow. 

What happens next:
• We'll keep you updated on our progress
• You'll get early access when we launch
• Exclusive beta testing opportunities
• Special launch pricing

{f"Expected launch: {launch_date}" if launch_date else "We'll announce the launch date soon!"}

Stay tuned for updates!

Best regards,
The {company_name} Team

---
You're receiving this because you signed up for our waitlist.
If you want to unsubscribe, reply with "UNSUBSCRIBE"."""

            html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to {product_name}</title>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
        .header {{ background: #f8f9fa; padding: 20px; text-align: center; border-radius: 8px; }}
        .content {{ padding: 20px 0; }}
        .footer {{ background: #f8f9fa; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
        .button {{ display: inline-block; padding: 12px 24px; background: #007bff; color: white; text-decoration: none; border-radius: 5px; }}
        ul {{ padding-left: 20px; }}
        li {{ margin-bottom: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Welcome to {product_name}!</h1>
            <p>You're on the waitlist 🎉</p>
        </div>
        
        <div class="content">
            <p>Hi there!</p>
            
            <p>Thank you for joining the <strong>{product_name}</strong> waitlist. We're thrilled to have you on board!</p>
            
            <p>{company_name} is working hard to bring you an amazing product that will revolutionize your workflow.</p>
            
            <h3>What happens next:</h3>
            <ul>
                <li>We'll keep you updated on our progress</li>
                <li>You'll get early access when we launch</li>
                <li>Exclusive beta testing opportunities</li>
                <li>Special launch pricing</li>
            </ul>
            
            {f"<p><strong>Expected launch:</strong> {launch_date}</p>" if launch_date else "<p>We'll announce the launch date soon!</p>"}
            
            <p>Stay tuned for updates!</p>
            
            <p>Best regards,<br>The {company_name} Team</p>
        </div>
        
        <div class="footer">
            <p>You're receiving this because you signed up for our waitlist.</p>
            <p>If you want to unsubscribe, reply with "UNSUBSCRIBE".</p>
        </div>
    </div>
</body>
</html>"""
            
            return {
                "success": True,
                "subject": subject,
                "content": content,
                "html_content": html_content
            }
            
        except Exception as e:
            logger.error(f"Failed to create waitlist email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
            
    def _send_via_sendgrid(self, to_email: str, subject: str, content: str, 
                          from_email: str, from_name: str, html_content: str) -> Dict[str, Any]:
        """Send email via SendGrid API"""
        
        if not self.api_key:
            return {
                "success": False,
                "error": "SendGrid API key not provided"
            }
            
        payload = {
            "personalizations": [{
                "to": [{"email": to_email}],
                "subject": subject
            }],
            "from": {
                "email": from_email or "noreply@example.com",
                "name": from_name or "Dream Machine"
            },
            "content": [
                {"type": "text/plain", "value": content}
            ]
        }
        
        if html_content:
            payload["content"].append({"type": "text/html", "value": html_content})
            
        response = requests.post(
            self.providers["sendgrid"]["api_url"],
            headers=self.providers["sendgrid"]["headers"],
            json=payload
        )
        
        if response.status_code == 202:
            return {"success": True, "message_id": response.headers.get("X-Message-Id")}
        else:
            return {"success": False, "error": response.text}
            
    def _send_via_mailgun(self, to_email: str, subject: str, content: str,
                         from_email: str, from_name: str, html_content: str) -> Dict[str, Any]:
        """Send email via Mailgun API"""
        
        if not self.api_key:
            return {
                "success": False,
                "error": "Mailgun API key not provided"
            }
            
        domain = "sandbox123.mailgun.org"  # Replace with your domain
        
        data = {
            "from": f"{from_name or 'Dream Machine'} <{from_email or f'noreply@{domain}'}>",
            "to": to_email,
            "subject": subject,
            "text": content
        }
        
        if html_content:
            data["html"] = html_content
            
        response = requests.post(
            f"{self.providers['mailgun']['api_url']}/{domain}/messages",
            auth=self.providers["mailgun"]["auth"],
            data=data
        )
        
        if response.status_code == 200:
            return {"success": True, "message_id": response.json().get("id")}
        else:
            return {"success": False, "error": response.text}
            
    def _send_via_smtp(self, to_email: str, subject: str, content: str,
                      from_email: str, from_name: str, html_content: str,
                      attachments: List[str]) -> Dict[str, Any]:
        """Send email via SMTP"""
        
        smtp_config = self.providers["smtp"]
        
        if not smtp_config["username"] or not smtp_config["password"]:
            return {
                "success": False,
                "error": "SMTP credentials not provided"
            }
            
        # Create message
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{from_name or 'Dream Machine'} <{from_email or smtp_config['username']}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Add text content
        text_part = MIMEText(content, 'plain')
        msg.attach(text_part)
        
        # Add HTML content
        if html_content:
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
        # Add attachments
        if attachments:
            for file_path in attachments:
                if os.path.exists(file_path):
                    with open(file_path, "rb") as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename= {os.path.basename(file_path)}'
                    )
                    msg.attach(part)
                    
        # Send email
        try:
            server = smtplib.SMTP(smtp_config["server"], smtp_config["port"])
            server.starttls()
            server.login(smtp_config["username"], smtp_config["password"])
            server.send_message(msg)
            server.quit()
            
            return {"success": True, "message": "Email sent successfully"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
            
    def _personalize_content(self, content: str, recipient: Dict[str, str]) -> str:
        """Personalize email content with recipient data"""
        
        if not content:
            return content
            
        personalized = content
        
        # Replace common placeholders
        replacements = {
            "{{name}}": recipient.get("name", "there"),
            "{{first_name}}": recipient.get("first_name", recipient.get("name", "there")),
            "{{email}}": recipient.get("email", ""),
            "{{company}}": recipient.get("company", "")
        }
        
        for placeholder, value in replacements.items():
            personalized = personalized.replace(placeholder, value)
            
        return personalized
        
    def _save_campaign(self, campaign: Dict[str, Any]) -> None:
        """Save campaign to storage"""
        
        os.makedirs("data/campaigns", exist_ok=True)
        
        with open(f"data/campaigns/{campaign['id']}.json", "w") as f:
            json.dump(campaign, f, indent=2)
            
    def _load_campaign(self, campaign_id: str) -> Optional[Dict[str, Any]]:
        """Load campaign from storage"""
        
        try:
            with open(f"data/campaigns/{campaign_id}.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
            
    def _save_sequence(self, sequence: Dict[str, Any]) -> None:
        """Save email sequence to storage"""
        
        os.makedirs("data/sequences", exist_ok=True)
        
        with open(f"data/sequences/{sequence['id']}.json", "w") as f:
            json.dump(sequence, f, indent=2)
            
    def _load_sequence(self, sequence_id: str) -> Optional[Dict[str, Any]]:
        """Load email sequence from storage"""
        
        try:
            with open(f"data/sequences/{sequence_id}.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return None
            
    def _save_sequence_instance(self, instance: Dict[str, Any]) -> None:
        """Save sequence instance to storage"""
        
        os.makedirs("data/sequence_instances", exist_ok=True)
        
        with open(f"data/sequence_instances/{instance['id']}.json", "w") as f:
            json.dump(instance, f, indent=2)
            
    def _send_sequence_email(self, instance: Dict[str, Any], email_index: int) -> Dict[str, Any]:
        """Send a specific email in a sequence"""
        
        sequence = self._load_sequence(instance["sequence_id"])
        if not sequence or email_index >= len(sequence["emails"]):
            return {"success": False, "error": "Invalid sequence or email index"}
            
        email_config = sequence["emails"][email_index]
        
        # Personalize content
        content = self._personalize_content(email_config["content"], instance["recipient_data"])
        html_content = self._personalize_content(email_config.get("html_content", ""), instance["recipient_data"])
        
        # Send email
        result = self.send_email(
            to_email=instance["recipient_email"],
            subject=email_config["subject"],
            content=content,
            html_content=html_content
        )
        
        # Update instance
        instance["emails_sent"].append({
            "email_index": email_index,
            "sent_at": datetime.now().isoformat(),
            "success": result["success"]
        })
        
        instance["current_step"] = email_index + 1
        
        if email_index == len(sequence["emails"]) - 1:
            instance["completed"] = True
            
        self._save_sequence_instance(instance)
        
        return result

# Example usage
def main():
    """Example usage of EmailManager"""
    
    # SMTP configuration
    smtp_config = {
        "server": "smtp.gmail.com",
        "port": 587,
        "username": "your-email@gmail.com",
        "password": "your-app-password"
    }
    
    manager = EmailManager(provider="smtp", smtp_config=smtp_config)
    
    # Create waitlist email
    waitlist_email = manager.create_waitlist_email(
        company_name="DreamCorp",
        product_name="Dream Machine",
        launch_date="Q2 2024"
    )
    
    print("Waitlist email created:")
    print(json.dumps(waitlist_email, indent=2))
    
    # Send email
    result = manager.send_email(
        to_email="user@example.com",
        subject=waitlist_email["subject"],
        content=waitlist_email["content"],
        html_content=waitlist_email["html_content"]
    )
    
    print("\nEmail send result:")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()