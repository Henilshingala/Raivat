import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings

logger = logging.getLogger(__name__)


def send_anti_spam_email(
    subject, html_content, text_content, recipient_email, from_email=None
):
 
    try:
        if from_email is None:
            from_email = settings.DEFAULT_FROM_EMAIL

        
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_email
        msg["To"] = recipient_email

        
        msg["X-Priority"] = "1"
        msg["X-MSMail-Priority"] = "High"
        msg["Importance"] = "high"
        msg["X-Mailer"] = "Raivat Stone System v2.0"
        msg["List-Unsubscribe"] = (
            "<mailto:info.raivatstones@gmail.com?subject=unsubscribe>"
        )
        msg["List-Unsubscribe-Post"] = "List-Unsubscribe=One-Click"
        msg["Precedence"] = "bulk"
        msg["X-Auto-Response-Suppress"] = "OOF, AutoReply"
        msg["Auto-Submitted"] = "auto-generated"

        
        msg["X-Report-Abuse"] = "Please report abuse here: info.raivatstones@gmail.com"
        msg["X-Feedback-ID"] = "password-reset:raivat-stone"
        msg["X-Campaign"] = "password-reset"
        msg["X-Entity-Ref-ID"] = "password-reset-otp"

        
        import time
        import uuid

        timestamp = int(time.time())
        unique_id = str(uuid.uuid4())[:8]
        msg["Message-ID"] = f"<password-reset-{timestamp}-{unique_id}@raivatstone.com>"

        
        from email.utils import formatdate

        msg["Date"] = formatdate(localtime=True)

        
        msg["Reply-To"] = "support@raivatstone.com"

        
        msg["Organization"] = "Raivat Stone"

        
        msg["Content-Type"] = 'multipart/alternative; boundary="boundary-string"'

        
        text_part = MIMEText(text_content, "plain", "utf-8")
        text_part.add_header("Content-Type", "text/plain; charset=UTF-8")
        msg.attach(text_part)

        html_part = MIMEText(html_content, "html", "utf-8")
        html_part.add_header("Content-Type", "text/html; charset=UTF-8")
        msg.attach(html_part)

        
        with smtplib.SMTP(
            settings.EMAIL_HOST, settings.EMAIL_PORT, timeout=30
        ) as server:
            server.set_debuglevel(0)  
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)


            server.sendmail(from_email, [recipient_email], msg.as_string())

        logger.info(f"Advanced anti-spam email sent successfully to {recipient_email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send anti-spam email to {recipient_email}: {str(e)}")
        return False


def create_password_reset_email(otp, user_email):
 
    subject = "Your Raivat Stone Password Reset Code"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta name="color-scheme" content="light">
        <meta name="supported-color-schemes" content="light">
        <title>Password Reset - Raivat Stone</title>
        <style>
            
            body, table, td, p, a, li, blockquote {{ -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }}
            table, td {{ mso-table-lspace: 0pt; mso-table-rspace: 0pt; }}
            img {{ -ms-interpolation-mode: bicubic; border: 0; outline: none; text-decoration: none; }}
            
            
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                color: #333333; 
                margin: 0; 
                padding: 0; 
                background-color: #f4f4f4;
                -webkit-font-smoothing: antialiased;
            }}
            
            .email-container {{ 
                max-width: 600px; 
                margin: 0 auto; 
                background: #ffffff;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            .header {{ 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                padding: 40px 30px; 
                text-align: center;
                position: relative;
            }}
            
            .header::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="rgba(255,255,255,0.1)"/><circle cx="75" cy="75" r="1" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
                opacity: 0.3;
            }}
            
            .header-content {{ position: relative; z-index: 1; }}
            
            .logo {{ 
                font-size: 28px; 
                font-weight: bold; 
                margin-bottom: 15px;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            
            .header h1 {{ 
                font-size: 24px; 
                margin: 0 0 10px 0;
                font-weight: 600;
                text-shadow: 0 2px 4px rgba(0,0,0,0.3);
            }}
            
            .header p {{ 
                margin: 0;
                opacity: 0.9;
                font-size: 16px;
            }}
            
            .content {{ 
                padding: 40px 30px; 
                background: #ffffff;
            }}
            
            .greeting {{
                font-size: 18px;
                color: #2c3e50;
                margin-bottom: 20px;
                font-weight: 500;
            }}
            
            .description {{
                color: #555555;
                margin-bottom: 30px;
                line-height: 1.7;
            }}
            
            .otp-container {{ 
                background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
                border: 2px solid #667eea; 
                border-radius: 12px; 
                padding: 30px 20px; 
                text-align: center; 
                margin: 30px 0;
                box-shadow: 0 4px 15px rgba(102, 126, 234, 0.15);
            }}
            
            .otp-label {{
                font-size: 16px;
                color: #495057;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            
            .otp-code {{ 
                font-size: 36px; 
                font-weight: bold; 
                color: #667eea; 
                letter-spacing: 8px; 
                font-family: 'Courier New', 'Monaco', monospace;
                background: #ffffff;
                padding: 15px 25px;
                border-radius: 8px;
                border: 2px solid #e9ecef;
                display: inline-block;
                margin: 10px 0;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            
            .otp-expiry {{
                font-size: 14px;
                color: #6c757d;
                margin-top: 15px;
                font-weight: 500;
            }}
            
            .security-section {{ 
                background: #fff3cd; 
                border: 1px solid #ffeaa7; 
                border-radius: 8px; 
                padding: 20px; 
                margin: 30px 0;
                border-left: 4px solid #ffc107;
            }}
            
            .security-title {{
                font-size: 16px;
                font-weight: 600;
                color: #856404;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            
            .security-list {{
                margin: 0;
                padding-left: 20px;
                color: #856404;
            }}
            
            .security-list li {{
                margin-bottom: 8px;
                line-height: 1.5;
            }}
            
            .support-section {{
                background: #e3f2fd;
                border: 1px solid #bbdefb;
                border-radius: 8px;
                padding: 20px;
                margin: 30px 0;
                text-align: center;
            }}
            
            .support-text {{
                color: #1565c0;
                font-weight: 500;
                margin: 0;
            }}
            
            .footer {{ 
                text-align: center; 
                margin-top: 40px; 
                color: #6c757d; 
                font-size: 13px; 
                padding: 30px;
                background: #f8f9fa;
                border-top: 1px solid #e9ecef;
            }}
            
            .footer p {{
                margin: 5px 0;
                line-height: 1.4;
            }}
            
            .footer-strong {{
                font-weight: 600;
                color: #495057;
            }}
            
            .unsubscribe {{
                color: #6c757d;
                text-decoration: underline;
            }}
            
                
            @media only screen and (max-width: 600px) {{
                .email-container {{
                    margin: 10px;
                    border-radius: 0;
                }}
                
                .header, .content, .footer {{
                    padding: 20px 15px;
                }}
                
                .otp-code {{
                    font-size: 28px;
                    letter-spacing: 6px;
                    padding: 12px 20px;
                }}
                
                .logo {{
                    font-size: 24px;
                }}
                
                .header h1 {{
                    font-size: 20px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <div class="header-content">
                    <div class="logo">💎 Raivat Stone</div>
                    <h1>🔐 Password Reset Code</h1>
                    <p>Secure Account Verification</p>
                </div>
            </div>
            
            <div class="content">
                <div class="greeting">Hello!</div>
                
                <div class="description">
                    We received a request to reset your password for your Raivat Stones account. 
                    To proceed with the password reset, please use the verification code below.
                </div>
                
                <div class="otp-container">
                    <div class="otp-label">Your Verification Code</div>
                    <div class="otp-code">{otp}</div>
                    <div class="otp-expiry">⏰ This code expires in 10 minutes</div>
                </div>
                
                <div class="security-section">
                    <div class="security-title">
                        🔒 Security Information
                    </div>
                    <ul class="security-list">
                        <li>This verification code will expire in 10 minutes for your security</li>
                        <li>If you didn't request this password reset, please ignore this email</li>
                        <li>Never share this code with anyone, including our support team</li>
                        <li>Our team will never ask for this code via phone or email</li>
                        <li>This email is sent from our secure, verified system</li>
                    </ul>
                </div>
                
                <div class="support-section">
                    <p class="support-text">
                        Need help? Contact our support team at support@raivatstone.com
                    </p>
                </div>
                
                <div class="footer">
                    <p class="footer-strong">Raivat Stones - Secure Authentication</p>
                    <p>This is an automated message from our secure system</p>
                    <p>© 2024 Raivat Stones. All rights reserved.</p>
                    <p>To unsubscribe from these emails, reply with "UNSUBSCRIBE" in the subject line</p>
                    <p>This email was sent to: {user_email}</p>
                    <p class="unsubscribe">If you're having trouble, please add us to your contacts</p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    text_content = f"""
    Raivat Stones - Password Reset Verification
    ============================================
    
    Hello!
    
    We received a request to reset your password for your Raivat Stones account.
    To proceed with the password reset, please use the verification code below.
    
    VERIFICATION CODE: {otp}
    
    This code expires in 10 minutes.
    
    SECURITY INFORMATION:
    - This verification code will expire in 10 minutes for your security
    - If you didn't request this password reset, please ignore this email
    - Never share this code with anyone, including our support team
    - Our team will never ask for this code via phone or email
    - This email is sent from our secure, verified system
    
    Need help? Contact our support team at support@raivatstone.com
    
    ============================================
    Raivat Stones - Secure Authentication
    This is an automated message from our secure system
    © 2024 Raivat Stones. All rights reserved.
    
    To unsubscribe from these emails, reply with "UNSUBSCRIBE" in the subject line.
    This email was sent to: {user_email}
    
    If you're having trouble receiving our emails, please add us to your contacts.
    """

    return subject, html_content, text_content
