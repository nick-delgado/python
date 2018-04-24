from django.shortcuts import render
from aircraft.models import Aircraft
from rest_framework import viewsets, generics
from aircraft.serializers import AircraftSerializer

# Create your views here.
class AircraftViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Aircraft.objects.all()
    serializer_class = AircraftSerializer


class AircraftList(generics.ListAPIView):
    """
    API endpoint that allows aircrafts to be selected.
    """

    serializer_class = AircraftSerializer
    def get_queryset(self):
        speed = self.kwargs['speed']
        return Aircraft.objects.filter(cruising_speed__gt=speed)
