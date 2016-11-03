from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .serializers import VVSDataSerializer
from .models import VVSData
import redis
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_201_CREATED
# Create your views here.


class VVSDataViewSet(ModelViewSet):
    serializer_class = VVSDataSerializer
    queryset = VVSData.objects.filter(delay__gte=0).order_by('-timestamp')

    def list_delays(self, request, *args, **kwargs):
        redis_connection = redis.StrictRedis(host='localhost', port=6379, db=1)
        keys = redis_connection.keys("*")
        if len(keys) > 0:
            delays = redis_connection.mget(keys)
            if len(delays) > 0:

                return JsonResponse(delays, safe=False)
        else:
            return Response(status=HTTP_404_NOT_FOUND)