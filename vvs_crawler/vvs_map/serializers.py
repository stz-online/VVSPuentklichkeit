from rest_framework.serializers import ModelSerializer
from .models import VVSData


class VVSDataSerializer(ModelSerializer):

    class Meta:
        model = VVSData
        fields = '__all__'