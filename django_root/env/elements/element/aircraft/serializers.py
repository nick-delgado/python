from aircraft.models import Aircraft
from rest_framework import serializers

class AircraftSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Aircraft
        fields = ('id', 'url', 'tailnumber', 'cruising_speed')
