import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView

from kudos.apps.kudo_app.api.serializers.user_profile import SerializerAPIUserProfile
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# ViewAPIUserProfile
#-------------------------------------------------------------------------------
class ViewAPIUserProfile(APIView):
    """
    API view for retrieving and updating user profile information.
    This view allows for getting and setting the user profile details.
    """

    serializer_class = SerializerAPIUserProfile

    def get(self, request):
        user = self.serializer_class(
            request.user,
            context={'request':request}
        ).data
        
        return Response(user, status=HTTP_200_OK)