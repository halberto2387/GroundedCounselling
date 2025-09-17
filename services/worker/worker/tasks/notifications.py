from typing import Dict, Any
from datetime import datetime, timedelta

from worker.tasks.email import (
    send_booking_confirmation_email,
    send_session_reminder_email,
    send_welcome_email,
)
from worker.tasks.sms import (
    send_booking_confirmation_sms,
    send_session_reminder_sms,
)
from worker.logging_setup import get_logger

logger = get_logger(__name__)


def send_booking_notifications(
    user_data: Dict[str, Any],
    booking_data: Dict[str, Any],
    notification_preferences: Dict[str, bool],
) -> Dict[str, Any]:
    """
    Send booking confirmation notifications via multiple channels.
    
    Args:
        user_data: User information (email, phone, name, etc.)
        booking_data: Booking details
        notification_preferences: User's notification preferences
        
    Returns:
        Dict with results from each notification channel
    """
    results = {}
    
    try:
        # Send email notification
        if notification_preferences.get("email", True) and user_data.get("email"):
            email_result = send_booking_confirmation_email(
                user_email=user_data["email"],
                user_name=user_data["name"],
                booking_details=booking_data,
            )
            results["email"] = email_result
        
        # Send SMS notification
        if notification_preferences.get("sms", False) and user_data.get("phone"):
            sms_result = send_booking_confirmation_sms(
                phone_number=user_data["phone"],
                booking_details=booking_data,
            )
            results["sms"] = sms_result
        
        logger.info(f"Booking notifications sent for booking {booking_data.get('id')}")
        return {"success": True, "results": results}
        
    except Exception as e:
        error_msg = f"Error sending booking notifications: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def send_session_reminders(
    user_data: Dict[str, Any],
    session_data: Dict[str, Any],
    notification_preferences: Dict[str, bool],
) -> Dict[str, Any]:
    """
    Send session reminder notifications.
    
    Args:
        user_data: User information
        session_data: Session details including video link
        notification_preferences: User's notification preferences
        
    Returns:
        Dict with results from each notification channel
    """
    results = {}
    
    try:
        # Send email reminder
        if notification_preferences.get("email", True) and user_data.get("email"):
            email_result = send_session_reminder_email(
                user_email=user_data["email"],
                user_name=user_data["name"],
                session_details=session_data,
            )
            results["email"] = email_result
        
        # Send SMS reminder
        if notification_preferences.get("sms", False) and user_data.get("phone"):
            sms_result = send_session_reminder_sms(
                phone_number=user_data["phone"],
                session_details=session_data,
            )
            results["sms"] = sms_result
        
        logger.info(f"Session reminders sent for session {session_data.get('id')}")
        return {"success": True, "results": results}
        
    except Exception as e:
        error_msg = f"Error sending session reminders: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def send_welcome_notifications(
    user_data: Dict[str, Any],
    notification_preferences: Dict[str, bool],
) -> Dict[str, Any]:
    """
    Send welcome notifications to new users.
    
    Args:
        user_data: New user information
        notification_preferences: User's notification preferences
        
    Returns:
        Dict with results from each notification channel
    """
    results = {}
    
    try:
        # Send welcome email
        if notification_preferences.get("email", True) and user_data.get("email"):
            email_result = send_welcome_email(
                user_email=user_data["email"],
                user_name=user_data["name"],
            )
            results["email"] = email_result
        
        logger.info(f"Welcome notifications sent for user {user_data.get('id')}")
        return {"success": True, "results": results}
        
    except Exception as e:
        error_msg = f"Error sending welcome notifications: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}


def process_scheduled_reminders() -> Dict[str, Any]:
    """
    Process scheduled session reminders.
    This would typically be called by a scheduler (e.g., cron job).
    
    Returns:
        Dict with processing results
    """
    try:
        # TODO: Implement database query to get sessions needing reminders
        # For now, this is a placeholder
        
        # Query for sessions starting in 24 hours that haven't had reminders sent
        # reminder_time = datetime.utcnow() + timedelta(hours=24)
        
        logger.info("Processing scheduled reminders")
        
        # Placeholder: In a real implementation, this would:
        # 1. Query database for upcoming sessions
        # 2. Check if reminders have already been sent
        # 3. Send reminders for eligible sessions
        # 4. Mark reminders as sent
        
        return {"success": True, "reminders_sent": 0}
        
    except Exception as e:
        error_msg = f"Error processing scheduled reminders: {str(e)}"
        logger.error(error_msg)
        return {"success": False, "error": error_msg}