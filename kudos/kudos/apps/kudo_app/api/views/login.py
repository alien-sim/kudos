import logging
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from kudos.apps.kudo_app.api.serializers.login import SerializerAPITokenView

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# ViewAPILogin
#-------------------------------------------------------------------------------
class ViewAPILogin(APIView):


    permission_classes = [AllowAny]
    serializer_class = SerializerAPITokenView

    def post(self, request):
        logger.debug('Attempting to login a user.')
        
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            response = serializer.get_tokens()
            
            return Response(response, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)