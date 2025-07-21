import logging
from functools import wraps

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


def bulletproof_auth_required(view_func):
 

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            logger.warning(f"Unauthenticated access attempt to {request.path}")
            return redirect("login")

        
        if request.user.is_anonymous:
            logger.warning(f"Anonymous user access attempt to {request.path}")
            request.session.flush()
            logout(request)
            messages.error(request, "Authentication required. Please log in.")
            return redirect("login")

        
        session_user_id = request.session.get("_auth_user_id")
        if not session_user_id or str(request.user.id) != str(session_user_id):
            logger.warning(
                f"Session mismatch for user {request.user.id} on {request.path}"
            )
            request.session.flush()
            logout(request)
            messages.error(request, "Session expired. Please log in again.")
            return redirect("login")

        
        try:
            from django.contrib.auth.models import User

            user = User.objects.get(id=request.user.id, is_active=True)
        except:
            logger.warning(f"Invalid user access attempt to {request.path}")
            request.session.flush()
            logout(request)
            messages.error(request, "Account not found or deactivated.")
            return redirect("login")

        
        if not hasattr(request.user, "id") or not request.user.id:
            logger.warning(f"Invalid user object on {request.path}")
            request.session.flush()
            logout(request)
            messages.error(request, "Authentication error. Please log in again.")
            return redirect("login")

        
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def secure_account_access(view_func):
    

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            logger.warning(
                f"SECURITY ALERT: Unauthenticated account access attempt to {request.path}"
            )
            return redirect("login")

        if request.user.is_anonymous:
            logger.warning(
                f"SECURITY ALERT: Anonymous account access attempt to {request.path}"
            )
            request.session.flush()
            logout(request)
            messages.error(
                request, "SECURITY: Authentication required for account access."
            )
            return redirect("login")

        session_user_id = request.session.get("_auth_user_id")
        if not session_user_id or str(request.user.id) != str(session_user_id):
            logger.warning(
                f"SECURITY ALERT: Session mismatch for account access {request.path}"
            )
            request.session.flush()
            logout(request)
            messages.error(request, "SECURITY: Session expired. Please log in again.")
            return redirect("login")

        try:
            from django.contrib.auth.models import User

            user = User.objects.get(id=request.user.id, is_active=True)
        except:
            logger.warning(
                f"SECURITY ALERT: Invalid user account access attempt to {request.path}"
            )
            request.session.flush()
            logout(request)
            messages.error(request, "SECURITY: Account not found or deactivated.")
            return redirect("login")


        logger.info(
            f"Secure account access granted to user {request.user.id} for {request.path}"
        )

        return view_func(request, *args, **kwargs)

    return _wrapped_view
