from enum import Enum
from typing import Any

from fastapi import HTTPException, status


class UserRole(str, Enum):
    """User roles for RBAC."""
    
    PATIENT = "patient"
    COUNSELLOR = "counsellor" 
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"


class Permission(str, Enum):
    """System permissions."""
    
    # User permissions
    READ_USER = "read:user"
    WRITE_USER = "write:user"
    DELETE_USER = "delete:user"
    
    # Specialist permissions
    READ_SPECIALIST = "read:specialist"
    WRITE_SPECIALIST = "write:specialist"
    DELETE_SPECIALIST = "delete:specialist"
    
    # Booking permissions
    READ_BOOKING = "read:booking"
    WRITE_BOOKING = "write:booking"
    DELETE_BOOKING = "delete:booking"
    
    # Session permissions
    READ_SESSION = "read:session"
    WRITE_SESSION = "write:session"
    DELETE_SESSION = "delete:session"
    
    # Content permissions
    READ_CONTENT = "read:content"
    WRITE_CONTENT = "write:content"
    DELETE_CONTENT = "delete:content"
    
    # Admin permissions
    ADMIN_USERS = "admin:users"
    ADMIN_SYSTEM = "admin:system"
    ADMIN_AUDIT = "admin:audit"


# Role permission mappings
ROLE_PERMISSIONS = {
    UserRole.PATIENT: {
        Permission.READ_USER,
        Permission.WRITE_USER,  # Own profile only
        Permission.READ_SPECIALIST,
        Permission.READ_BOOKING,  # Own bookings only
        Permission.WRITE_BOOKING,  # Own bookings only
        Permission.READ_SESSION,  # Own sessions only
        Permission.READ_CONTENT,
    },
    UserRole.COUNSELLOR: {
        Permission.READ_USER,
        Permission.WRITE_USER,  # Own profile only
        Permission.READ_SPECIALIST,
        Permission.WRITE_SPECIALIST,  # Own profile only
        Permission.READ_BOOKING,
        Permission.WRITE_BOOKING,
        Permission.READ_SESSION,
        Permission.WRITE_SESSION,
        Permission.READ_CONTENT,
        Permission.WRITE_CONTENT,
    },
    UserRole.ADMIN: {
        Permission.READ_USER,
        Permission.WRITE_USER,
        Permission.DELETE_USER,
        Permission.READ_SPECIALIST,
        Permission.WRITE_SPECIALIST,
        Permission.DELETE_SPECIALIST,
        Permission.READ_BOOKING,
        Permission.WRITE_BOOKING,
        Permission.DELETE_BOOKING,
        Permission.READ_SESSION,
        Permission.WRITE_SESSION,
        Permission.DELETE_SESSION,
        Permission.READ_CONTENT,
        Permission.WRITE_CONTENT,
        Permission.DELETE_CONTENT,
        Permission.ADMIN_USERS,
        Permission.ADMIN_AUDIT,
    },
    UserRole.SUPER_ADMIN: {
        # Super admin has all permissions
        *Permission.__members__.values()
    },
}


def check_permission(user_role: UserRole, required_permission: Permission) -> bool:
    """Check if a user role has the required permission."""
    return required_permission in ROLE_PERMISSIONS.get(user_role, set())


def require_permission(user_role: UserRole, required_permission: Permission) -> None:
    """Raise an exception if the user doesn't have the required permission."""
    if not check_permission(user_role, required_permission):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Permission denied. Required: {required_permission.value}"
        )