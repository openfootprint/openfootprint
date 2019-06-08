from rest_framework import serializers
from .models import Project, Extra, Transport, Footprint, Person, Tag, Location, Address


# TODO: filter fields properly

class ExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extra
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("source_name", "source_country", "id", "latitude", "longitude", "country")


class LocationSerializer(serializers.ModelSerializer):
    address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Location
        fields = '__all__'


class TransportSerializer(serializers.ModelSerializer):
    to_address = AddressSerializer(many=False, read_only=True)
    from_address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Transport
        fields = '__all__'


class FootprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Footprint
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):

    home_address = AddressSerializer(many=False, read_only=True)

    class Meta:
        model = Person
        fields = '__all__'


class ProjectSerializerFull(serializers.ModelSerializer):
    extras = ExtraSerializer(many=True, read_only=True)
    transports = TransportSerializer(many=True, read_only=True)
    footprints = FootprintSerializer(many=True, read_only=True)
    people = PersonSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    locations = LocationSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'

class ProjectSerializerList(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = ('id', 'name', 'kind')
