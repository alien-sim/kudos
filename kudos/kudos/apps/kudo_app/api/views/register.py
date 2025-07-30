import logging
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from kudos.kudos.apps.kudo_app.api.serializers.register import SerializerAPIRegister

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# ViewAPIRegister
#-------------------------------------------------------------------------------
class ViewAPIRegister(APIView):
    """ Creating a New User"""

    permission_classes = [AllowAny]
    serializer_class = SerializerAPIRegister

    def post(self, request):
        
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():

            serializer.register()
            
            return Response({}, status=HTTP_200_OK)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)