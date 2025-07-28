import logging
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# User
#-------------------------------------------------------------------------------
class User(AbstractUser):
    """
    Custom User model extending Django's AbstractUser
    """
    email = models.EmailField(
        unique=True
    )

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
    
    #---------------------------------------------------------------------------
    # get_access_tokens
    #---------------------------------------------------------------------------
    def get_access_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }