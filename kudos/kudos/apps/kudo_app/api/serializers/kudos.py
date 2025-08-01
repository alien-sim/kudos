from datetime import timedelta
import logging
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.models.kudo import Kudo
from kudos.apps.kudo_app.models.kudo_tracker import WeeklyKudoTracker
from kudos.apps.kudo_app.utility import get_week_start
from kudos.apps.kudo_app.api.serializers.user_profile import SerializerAPIUserProfile

logger = logging.getLogger(__name__)

#-------------------------------------------------------------------------------
# SerializerKudoModel
#-------------------------------------------------------------------------------
class SerializerKudoModel(serializers.ModelSerializer):

    sender = serializers.SerializerMethodField()
    receiver = serializers.SerializerMethodField()

    class Meta:
        model = Kudo
        fields = '__all__'

    def get_sender(self, kudo):
        return SerializerAPIUserProfile(
            kudo.sender,
            context=self.context
        ).data
    
    def get_receiver(self, kudo):
        return SerializerAPIUserProfile(
            kudo.receiver,
            context=self.context
        ).data

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

        
