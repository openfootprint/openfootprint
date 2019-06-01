from rest_framework import serializers
from .models import Project, Extra, Transport, Footprint, Person, Tag, Location


# TODO: filter fields properly

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ("source_name", "source_country", "id", "latitude", "longitude", "country")


class TransportSerializer(serializers.ModelSerializer):
    to_location = LocationSerializer(many=False, read_only=True)
    from_location = LocationSerializer(many=False, read_only=True)

    class Meta:
        model = Transport
        fields = '__all__'


class FootprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footprint
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'


class ProjectSerializerFull(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True, read_only=True)
    transports = TransportSerializer(many=True, read_only=True)
    footprints = FootprintSerializer(many=True, read_only=True)
    persons = PersonSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'kind')
