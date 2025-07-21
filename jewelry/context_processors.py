import logging

from django.contrib.auth.models import AnonymousUser

logger = logging.getLogger(__name__)


def security_context(request):
 
    context = {}

    admin_emails = [
        "info.raivatstones@gmail.com",
        "admin@raivatstone.com",
    ]

    if request.path.startswith("/account/"):
        logger.warning(
            f"SECURITY: Ultra-strict context check for account page: {request.path}"
        )

        context["user_is_authenticated"] = False
        context["user_is_anonymous"] = True
        context["user_has_valid_session"] = False
        context["user_id"] = None
        context["user_email"] = None
        context["session_user_id"] = None
        context["session_valid"] = False

        if hasattr(request, "user") and request.user.is_authenticated:
            session_user_id = request.session.get("_auth_user_id")

            if hasattr(request.user, "email") and request.user.email in admin_emails:
                logger.warning(
                    f"SECURITY: Admin user {request.user.email} blocked from website context"
                )
                return context

            if (
                session_user_id
                and str(request.user.id) == str(session_user_id)
                and hasattr(request.user, "id")
                and hasattr(request.user, "email")
                and request.user.email
            ):

                try:
                    from django.contrib.auth.models import User

                    user = User.objects.get(id=request.user.id, is_active=True)
                    if user.email == request.user.email:
                        logger.info(
                            f"SECURITY: Perfect validation passed for user {user.email}"
                        )
                        context["user_is_authenticated"] = True
                        context["user_is_anonymous"] = False
                        context["user_has_valid_session"] = True
                        context["user_id"] = request.user.id
                        context["user_email"] = request.user.email
                        context["session_user_id"] = session_user_id
                        context["session_valid"] = True
                    else:
                        logger.warning(
                            f"SECURITY: Email mismatch for user {request.user.id}"
                        )
                except:
                    logger.warning(
                        f"SECURITY: Database validation failed for user {request.user.id}"
                    )
            else:
                logger.warning(f"SECURITY: Session validation failed for account page")

        return context

    if hasattr(request, "user"):
        if not request.user.is_authenticated:
            if not isinstance(request.user, AnonymousUser):
                logger.warning(
                    f"Security: Invalid user object detected on {request.path}"
                )
                request.user = AnonymousUser()

        if (
            request.user.is_authenticated
            and hasattr(request.user, "email")
            and request.user.email in admin_emails
        ):
            logger.warning(
                f"SECURITY: Admin user {request.user.email} blocked from website context"
            )
            context["user_is_authenticated"] = False
            context["user_is_anonymous"] = True
            context["user_has_valid_session"] = False
            context["user_id"] = None
            context["user_email"] = None
            context["session_user_id"] = None
            context["session_valid"] = False
            return context

        context["user_is_authenticated"] = request.user.is_authenticated
        context["user_is_anonymous"] = request.user.is_anonymous
        context["user_has_valid_session"] = bool(request.session.get("_auth_user_id"))

        
        if request.user.is_authenticated:
            context["user_id"] = getattr(request.user, "id", None)
            context["user_email"] = getattr(request.user, "email", None)
            context["session_user_id"] = request.session.get("_auth_user_id")

            
            session_user_id = request.session.get("_auth_user_id")
            if session_user_id and str(request.user.id) != str(session_user_id):
                logger.warning(f"Security: Session mismatch detected on {request.path}")
                context["session_valid"] = False
            else:
                context["session_valid"] = True
        else:
                
            context["user_id"] = None
            context["user_email"] = None
            context["session_user_id"] = None
            context["session_valid"] = False

    return context
