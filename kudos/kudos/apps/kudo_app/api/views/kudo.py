import logging

from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from kudos.apps.kudo_app.api.serializers.kudos import SerializerKudo
logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# ViewAPIKudo
#-------------------------------------------------------------------------------
class ViewAPIKudo(APIView):
    """
    View to send kudos from one user to another
    """
    
    def post(self, request, *args, **kwargs):
        
        serializer = SerializerKudo(
            data=request.data,
            context={'request':request}
        )
        try:
            if serializer.is_valid():
                response = serializer.save()
                return Response(response, status=HTTP_200_OK)
            
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({"reciever": e}, status=HTTP_400_BAD_REQUEST)

    
        
