import logging

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)


class AuthenticationEnforcementMiddleware:


    def __init__(self, get_response):
        self.get_response = get_response

        self.protected_urls = [
            "/account/",
            "/checkout/",
            "/order-confirmation/",
        ]


        self.sensitive_urls = [
            "/account/",
        ]

    def __call__(self, request):

        current_path = request.path


        if any(current_path.startswith(url) for url in self.sensitive_urls):
            self._enforce_authentication(request)

        response = self.get_response(request)
        return response

    def _enforce_authentication(self, request):


        if not request.user.is_authenticated:
            self._redirect_to_login(request)
            return


        if isinstance(request.user, AnonymousUser):
            self._redirect_to_login(request)
            return


        try:
            from django.contrib.auth.models import User

            user = User.objects.get(id=request.user.id, is_active=True)
        except:
            self._redirect_to_login(request)
            return

    def _redirect_to_login(self, request):
            
        messages.error(request, "Please log in to access this page.")
        return redirect("login")
