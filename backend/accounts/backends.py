from django.contrib.auth.backends import ModelBackend
from accounts.models import User


class EmailBackend(ModelBackend):
    """
    Authenticate by email. Accepts the identifier under either `username` or
    `email`, since Django's admin and various auth helpers pass it as `username`.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # Accept whichever parameter name was used — admin sends `username`,
        # some custom code may send `email`.
        email = username or kwargs.get('email')

        if not email or not password:
            return None

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user

        return None