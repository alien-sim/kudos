import logging
from rest_framework import serializers
from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.api.serializers.organization import SerializerAPIModelOrganization
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# SerializerAPIUserProfile
#-------------------------------------------------------------------------------
class SerializerAPIUserProfile(serializers.ModelSerializer):
    """
    Serializer for user profile information.
    """

    organization = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "organization")

    def get_organization(self, user):
        print("njfew")
        return SerializerAPIModelOrganization(
            user.organization
        ).data