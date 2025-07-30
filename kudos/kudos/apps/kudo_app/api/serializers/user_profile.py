import logging
from rest_framework import serializers
from kudos.apps.kudo_app.models.user import User
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# SerializerAPIUserProfile
#-------------------------------------------------------------------------------
class SerializerAPIUserProfile(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """
    
    class Meta:
        model = User
        fields = "__all__"