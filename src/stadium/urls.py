from django.urls import path, include
from rest_framework.routers import DefaultRouter

from stadium.views import StadiumViewSet, StadiumBookingViewSet

router = DefaultRouter()
router.register('stadium', StadiumViewSet, 'stadium')
router.register('stadium_booking', StadiumBookingViewSet, 'stadium_booking')


urlpatterns = [
    path('', include(router.urls)),
]
