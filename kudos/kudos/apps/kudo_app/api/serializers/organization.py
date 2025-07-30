from rest_framework import serializers
from kudos.apps.kudo_app.models.organization import Organization


class SerializerAPIModelOrganization(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('id','name')