from rest_framework import serializers
from Core.models import Business


class BusinessSerializers(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = '__all__'
