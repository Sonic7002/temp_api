# this file contains rbac dependencies

from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.api.dependencies.auth_deps import get_current_user
from app.schemas.user import UserRole

def require_role(*allowed_roles: UserRole):
    """takes different user roles and matches them with the current user using role_checker method"""
    def role_checker(current_user: User = Depends(get_current_user)):
        """checks the role using current user jwt and required role"""
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        return current_user
    return role_checker
