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
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "full_name", "organization")

    def get_full_name(self, user):
        return f"{user.first_name} {user.last_name}"

    def get_organization(self, user):
        print("njfew")
        return SerializerAPIModelOrganization(
            user.organization
        ).data