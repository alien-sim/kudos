import logging

from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from kudos.kudos.apps.kudo_app.api.serializers.kudos import SerializerKudo
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
        
        if serializer.is_valid():
            return Response(True, status=HTTP_200_OK)
    
        if 'X-TOKEN-AUTHENTICATION'.lower() in request.headers:
            error = {
                'email' : 'We already have an account with that email.',
            }
            return JsonResponse(error, status=HTTP_400_BAD_REQUEST)
        
        return JsonResponse(serializer.errors, status=HTTP_400_BAD_REQUEST)
