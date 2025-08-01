import logging
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.models.organization import Organization
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# SerializerAPIRegister
#-------------------------------------------------------------------------------
class SerializerAPIRegister(serializers.Serializer):
    """
    Represents login data.
    """
    
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    organization = serializers.IntegerField()
    
    #---------------------------------------------------------------------------
    # validate
    #---------------------------------------------------------------------------
    def validate(self, attrs): 
        email = attrs['email'].lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "This email is already registered."
            )
        try:
            self.organization = Organization.objects.get(
                id=attrs['organization']
            )
        except ObjectDoesNotExist:
            raise ValidationError(
                "Invalid Organization Error"
            )
        
        return super().validate(attrs)

    def register(self) -> None:

        User.objects.create_user(
            email=self.validated_data['email'],
            username=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            password=self.validated_data['password'],
            organization=self.organization
        )

        