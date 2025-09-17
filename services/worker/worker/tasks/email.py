from typing import Dict, Any, Optional
import httpx

from worker.config import settings
from worker.logging_setup import get_logger

logger = get_logger(__name__)


def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None,
    from_email: str = "noreply@groundedcounselling.com",
    from_name: str = "GroundedCounselling",
) -> Dict[str, Any]:
    """
    Send email using Resend API.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        html_content: HTML email content
        text_content: Plain text email content (optional)
        from_email: Sender email address
        from_name: Sender name
        
    Returns:
        Dict containing the result of the email send operation
    """
    if not settings.RESEND_API_KEY:
        logger.error("RESEND_API_KEY not configured")
        return {"success": False, "error": "Email service not configured"}
    
    try:
        # Prepare email data
        email_data = {
            "from": f"{from_name} <{from_email}>",
            "to": [to_email],
            "subject": subject,
            "html": html_content,
        }
        
        if text_content:
            email_data["text"] = text_content
        
        # Send email via Resend API
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        }
        
        with httpx.Client() as client:
            response = client.post(
                "https://api.resend.com/emails",
                json=email_data,
                headers=headers,
                timeout=30.0,
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Email sent successfully to {to_email}", email_id=result.get("id"))
                return {"success": True, "email_id": result.get("id")}
            else:
                error_msg = f"Failed to send email: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
                
    except Exception as e:
        error_msg = f"Error sending email: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def send_welcome_email(user_email: str, user_name: str) -> Dict[str, Any]:
    """Send welcome email to new user."""
    subject = "Welcome to GroundedCounselling"
    html_content = f"""
    <html>
        <body>
            <h1>Welcome to GroundedCounselling, {user_name}!</h1>
            <p>Thank you for joining our platform. We're excited to support you on your mental health journey.</p>
            <p>Here's what you can do next:</p>
            <ul>
                <li>Complete your profile</li>
                <li>Browse our qualified specialists</li>
                <li>Book your first session</li>
            </ul>
            <p>If you have any questions, don't hesitate to reach out to our support team.</p>
            <p>Best regards,<br>The GroundedCounselling Team</p>
        </body>
    </html>
    """
    text_content = f"""
    Welcome to GroundedCounselling, {user_name}!
    
    Thank you for joining our platform. We're excited to support you on your mental health journey.
    
    Here's what you can do next:
    - Complete your profile
    - Browse our qualified specialists
    - Book your first session
    
    If you have any questions, don't hesitate to reach out to our support team.
    
    Best regards,
    The GroundedCounselling Team
    """
    
    return send_email(
        to_email=user_email,
        subject=subject,
        html_content=html_content,
        text_content=text_content,
    )


def send_booking_confirmation_email(
    user_email: str,
    user_name: str,
    booking_details: Dict[str, Any],
) -> Dict[str, Any]:
    """Send booking confirmation email."""
    subject = "Booking Confirmation - GroundedCounselling"
    html_content = f"""
    <html>
        <body>
            <h1>Booking Confirmed</h1>
            <p>Hi {user_name},</p>
            <p>Your session has been confirmed! Here are the details:</p>
            <ul>
                <li><strong>Specialist:</strong> {booking_details.get('specialist_name')}</li>
                <li><strong>Date & Time:</strong> {booking_details.get('start_time')}</li>
                <li><strong>Duration:</strong> {booking_details.get('duration_minutes')} minutes</li>
                <li><strong>Session Type:</strong> Video Call</li>
            </ul>
            <p>You'll receive a reminder 24 hours before your session with the video call link.</p>
            <p>If you need to reschedule or cancel, please do so at least 24 hours in advance.</p>
            <p>Best regards,<br>The GroundedCounselling Team</p>
        </body>
    </html>
    """
    
    return send_email(
        to_email=user_email,
        subject=subject,
        html_content=html_content,
    )


def send_session_reminder_email(
    user_email: str,
    user_name: str,
    session_details: Dict[str, Any],
) -> Dict[str, Any]:
    """Send session reminder email."""
    subject = "Session Reminder - Tomorrow at GroundedCounselling"
    html_content = f"""
    <html>
        <body>
            <h1>Session Reminder</h1>
            <p>Hi {user_name},</p>
            <p>This is a friendly reminder about your upcoming session:</p>
            <ul>
                <li><strong>Specialist:</strong> {session_details.get('specialist_name')}</li>
                <li><strong>Date & Time:</strong> {session_details.get('start_time')}</li>
                <li><strong>Duration:</strong> {session_details.get('duration_minutes')} minutes</li>
            </ul>
            <p><strong>Join Link:</strong> <a href="{session_details.get('video_link')}">Click here to join your session</a></p>
            <p>Please join the video call a few minutes early to ensure everything is working properly.</p>
            <p>Looking forward to seeing you!<br>The GroundedCounselling Team</p>
        </body>
    </html>
    """
    
    return send_email(
        to_email=user_email,
        subject=subject,
        html_content=html_content,
    )