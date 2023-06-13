from rest_framework import serializers

from stadium.models import StadiumBooking


class StadiumBookingCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StadiumBooking
        fields = (
            'id',
            'stadium',
            'start_time',
            'end_time',
        )

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    @staticmethod
    def validate_start_time(value):  # TODO
        return value

    @staticmethod
    def validate_end_time(value):  # TODO
        return value


class StadiumBookingDetailSerializer(serializers.ModelSerializer):
    stadium = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = StadiumBooking
        fields = (
            'id',
            'stadium',
            'user',
            'start_time',
            'end_time',
        )

    @staticmethod
    def get_stadium(obj):
        return obj.stadium.name

    @staticmethod
    def get_user(obj):
        return obj.user.username
