from typing import Dict, Any
import httpx

from worker.config import settings
from worker.logging_setup import get_logger

logger = get_logger(__name__)


def send_sms(phone_number: str, message: str) -> Dict[str, Any]:
    """
    Send SMS using Twilio API.
    
    Args:
        phone_number: Recipient phone number (E.164 format)
        message: SMS message content
        
    Returns:
        Dict containing the result of the SMS send operation
    """
    if not all([settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER]):
        logger.error("Twilio credentials not fully configured")
        return {"success": False, "error": "SMS service not configured"}
    
    try:
        # Prepare SMS data
        sms_data = {
            "From": settings.TWILIO_PHONE_NUMBER,
            "To": phone_number,
            "Body": message,
        }
        
        # Send SMS via Twilio API
        auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"
        
        with httpx.Client() as client:
            response = client.post(
                url,
                data=sms_data,
                auth=auth,
                timeout=30.0,
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"SMS sent successfully to {phone_number}", message_sid=result.get("sid"))
                return {"success": True, "message_sid": result.get("sid")}
            else:
                error_msg = f"Failed to send SMS: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"success": False, "error": error_msg}
                
    except Exception as e:
        error_msg = f"Error sending SMS: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def send_booking_confirmation_sms(phone_number: str, booking_details: Dict[str, Any]) -> Dict[str, Any]:
    """Send booking confirmation SMS."""
    message = f"""GroundedCounselling: Your session with {booking_details.get('specialist_name')} is confirmed for {booking_details.get('start_time')}. You'll receive a reminder 24hrs before with the video link."""
    
    return send_sms(phone_number, message)


def send_session_reminder_sms(phone_number: str, session_details: Dict[str, Any]) -> Dict[str, Any]:
    """Send session reminder SMS."""
    message = f"""GroundedCounselling Reminder: Your session with {session_details.get('specialist_name')} is tomorrow at {session_details.get('start_time')}. Join here: {session_details.get('video_link')}"""
    
    return send_sms(phone_number, message)


def send_2fa_code_sms(phone_number: str, code: str) -> Dict[str, Any]:
    """Send 2FA verification code via SMS."""
    message = f"GroundedCounselling: Your verification code is {code}. This code expires in 5 minutes."
    
    return send_sms(phone_number, message)