from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import VVSDataSerializer
from .models import VVSData
# Create your views here.


class VVSDataViewSet(ModelViewSet):
    serializer_class = VVSDataSerializer
    queryset = VVSData.objects.filter(delay__gte=0).order_by('-timestamp')