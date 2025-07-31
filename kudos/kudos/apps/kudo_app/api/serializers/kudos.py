from datetime import timedelta
import logging
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.models.kudo import Kudo
from kudos.apps.kudo_app.models.kudo_tracker import WeeklyKudoTracker
from kudos.apps.kudo_app.utility import get_week_start

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# SerializerKudo
#-------------------------------------------------------------------------------
class SerializerKudo(serializers.Serializer):
    """
    Represents an to send Kudo to another with message.
    """
    
    reciever = serializers.IntegerField()
    message = serializers.CharField()
    
    #---------------------------------------------------------------------------
    # validate_reciever
    #---------------------------------------------------------------------------
    def validate_reciever(self, id):
        """
        Make sure emails are unique.
        """
        try:
            self.receiver = User.objects.get(
                id=id
            )
        except ObjectDoesNotExist:
            raise ValidationError(
                "Invalid Reciever ID"
            )
        if id == self.context['request'].user.id:
            raise ValidationError(
                "Cannot give Kudo to yourself"
            )

        kudo_exist = Kudo.kudo_sent_this_week(self.context['request'].user.id, id)
        if kudo_exist:
            raise ValidationError(
                "Kudo already given to this user"
            )
        return id
    
    def save(self):
        Kudo.send_kudo(
            sender=self.context['request'].user.id,
            receiver=self.validated_data['reciever'],
            message=self.validated_data['message']
        )
        return "Success"

        
