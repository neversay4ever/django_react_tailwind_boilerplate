from .models import APItest
from .serializers import APItestSerializer
from rest_framework import generics


class APItestListCreate(generics.ListCreateAPIView):
    queryset = APItest.objects.all()
    serializer_class = APItestSerializer
