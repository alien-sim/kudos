from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from kudos.apps.kudo_app.models.organization import Organization
from kudos.apps.kudo_app.api.serializers.organization import SerializerAPIModelOrganization


class ViewAPIOrganization(ListAPIView):
    permission_classes = (AllowAny,)
    pagination_class = None
    serializer_class = SerializerAPIModelOrganization
    queryset = Organization.objects.all()