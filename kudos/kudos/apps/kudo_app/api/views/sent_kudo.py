from datetime import timedelta
import logging

from rest_framework.generics import ListAPIView

from kudos.apps.kudo_app.utility import get_week_start
from kudos.apps.kudo_app.models.kudo import Kudo
from kudos.apps.kudo_app.api.serializers.kudos import SerializerKudoModel

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# ViewAPISentKudo
#-------------------------------------------------------------------------------
class ViewAPISentKudo(ListAPIView):
    """ List of users who you have sent this week"""

    serializer_class = SerializerKudoModel
    pagination_class = None

    def get_queryset(self):
        week_start = get_week_start()
        next_week_start = week_start + timedelta(days=7)
        print(week_start)
        return Kudo.objects.filter(
            sender_id=self.request.user,
            created_at__date__gte=week_start,
            created_at__date__lt=next_week_start
        )