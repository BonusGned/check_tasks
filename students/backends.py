from django.contrib.auth.backends import ModelBackend, BaseBackend
from django.db.models.query_utils import Q

from .models import User


class CustomModelBackend(BaseBackend):

    # Custom authenticate with phone or email
    def authenticate(self, request, **kwargs):
        try:
            user = CustomUser.objects.get(email__iexact=kwargs.get('email'))
        except CustomUser.DoesNotExist:
            return None
        return super().authenticate(request, **kwargs)

    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None