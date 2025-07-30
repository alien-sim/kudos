import logging
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import serializers

from kudos.apps.kudo_app.models.user import User
from kudos.apps.kudo_app.models.kudo import Kudo

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
        return id
    
    def save(self):
        Kudo.objects.create(
            sender_id=self.context['request'].user.id,
            reciever_id=self.validated_data['reciever'],
            message=self.validated_data['message'],
        )
        
