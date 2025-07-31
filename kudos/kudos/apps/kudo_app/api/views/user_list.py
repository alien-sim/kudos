import logging

from rest_framework.generics import ListAPIView

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.api.serializers.user_profile import SerializerAPIUserProfile

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# ViewAPIOrganizationUser
#-------------------------------------------------------------------------------
class ViewAPIOrganizationUser(ListAPIView):
    """ List of users belonging to given organization"""

    serializer_class = SerializerAPIUserProfile
    pagination_class = None

    def get_queryset(self):

        return User.objects.filter(
            organization=self.request.user.organization
        ).exclude(
            id=self.request.user.id
        )