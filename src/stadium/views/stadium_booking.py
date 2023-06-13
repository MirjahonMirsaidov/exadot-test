from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from core.utils.pagination import CustomPagination
from core.utils.permissions import IsVendor, IsUser
from stadium.models import StadiumBooking
from stadium.serializers.stadium_booking import StadiumBookingCreateSerializer, StadiumBookingDetailSerializer
from userprofile.models.userprofile import RoleChoices


class StadiumBookingViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return StadiumBookingCreateSerializer
        elif self.action == 'list':
            return StadiumBookingDetailSerializer

    def get_queryset(self):
        if self.request.user.role == RoleChoices.VENDOR:
            return StadiumBooking.objects.filter(stadium__vendor=self.request.user)
        elif self.request.user.role == RoleChoices.USER:
            return StadiumBooking.objects.filter(user=self.request.user)
        return StadiumBooking.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return IsUser(),
        elif self.action == 'destroy':
            return IsVendor(),
        return IsAuthenticated(),








