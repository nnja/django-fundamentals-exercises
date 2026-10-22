from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """The site's user account, with the same fields as the built-in user."""
