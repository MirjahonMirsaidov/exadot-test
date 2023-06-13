from django.contrib.gis.geos import Point
from rest_framework import serializers

from stadium.models import Stadium


class StadiumCUSerializer(serializers.ModelSerializer):
    lat = serializers.FloatField(required=True)
    lon = serializers.FloatField(required=True)

    class Meta:
        model = Stadium
        fields = (
            'id',
            'name',
            'address',
            'contact',
            'price_per_hour',
            'lat',
            'lon',
        )

    def create(self, validated_data):
        lat = validated_data.pop('lat')
        lon = validated_data.pop('lon')
        validated_data['location'] = Point(lon, lat)
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        lat = validated_data.pop('lat')
        lon = validated_data.pop('lon')
        validated_data['location'] = Point(lon, lat)
        return super().update(instance, validated_data)


class StadiumDetailSerializer(serializers.ModelSerializer):
    lat = serializers.ReadOnlyField()
    lon = serializers.ReadOnlyField()

    class Meta:
        model = Stadium
        fields = (
            'id',
            'name',
            'address',
            'contact',
            'price_per_hour',
            'lat',
            'lon',
        )
