import logging
from django.conf import settings
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import AbstractUser, UserManager
from kudos.apps.kudo_app.models.organization import Organization

logger = logging.getLogger(__name__)


class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(
        unique=True
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="users",
        help_text="Organization associated with the User",
        null=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        """
        String representation of the user object to display the user's email address.
        """
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def get_access_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }