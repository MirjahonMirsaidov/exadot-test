from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django_filters import FilterSet, BooleanFilter, DateTimeFilter

from stadium.models import Stadium


class StadiumFilter(FilterSet):
    start_time = DateTimeFilter(method='filter_start_time')
    order_by_distance = BooleanFilter(method='filter_order_by_distance')

    class Meta:
        model = Stadium
        fields = (
            'start_time',
            'order_by_distance',
        )

    def filter_order_by_distance(self, queryset, name, value):
        if value:
            # Retrieve the query parameters from the request object
            lon = float(self.request.query_params.get('lon', 0))
            lat = float(self.request.query_params.get('lat', 0))

            # Create a Point object for the user's current location
            user_location = Point(lon, lat, srid=4326)

            # Filter the queryset based on the distance from the user's location
            queryset = queryset.annotate(distance=Distance('location', user_location))

            return queryset.order_by('distance')
        return queryset

    def filter_start_time(self, queryset, name, value):
        end_time = self.request.query_params.get('end_time', None)
        if end_time is None:
            raise ValueError('end_time is required')
        return queryset.exclude(
            stadium_booking__start_time__lt=self.request.query_params.get('end_time', None),
            stadium_booking__end_time__gt=value
        )


