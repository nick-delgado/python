from django.shortcuts import render
from aircraft import Aircraft
from rest_framework import viewsets
from aircraft.serializers import AircraftSerializer

# Create your views here.
class AircraftViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer
