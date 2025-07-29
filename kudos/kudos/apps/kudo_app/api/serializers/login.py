import logging
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from kudos.apps.kudo_app.models.user import User
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# SerializerAPITokenView
#-------------------------------------------------------------------------------
class SerializerAPITokenView(serializers.Serializer):
    """
    Represents login data.
    """
    
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=30)
    
    #---------------------------------------------------------------------------
    # validate
    #---------------------------------------------------------------------------
    def validate(self, attrs): 
        try :
            email = attrs['email'].lower()
            self.user = User.objects.get(email=email)
        except (ObjectDoesNotExist, AttributeError):
            raise serializers.ValidationError('Invalid email or password.')
        
        if not self.user.check_password(attrs['password']):
            raise serializers.ValidationError('Invalid email or password.')
        
        if self.user.is_active == False:
            raise serializers.ValidationError('This user is not active.')

        
        return serializers.Serializer.validate(self, attrs)

    def login(self):
        return self.user.get_access_tokens()
        