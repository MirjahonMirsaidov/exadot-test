from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.utils.pagination import CustomPagination
from core.utils.permissions import IsVendor
from stadium.filters.stadium import StadiumFilter
from stadium.models import Stadium
from stadium.serializers.stadium import StadiumCUSerializer, StadiumDetailSerializer
from userprofile.models.userprofile import RoleChoices


class StadiumViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    filterset_class = StadiumFilter

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return StadiumCUSerializer
        elif self.action in ['list', 'retrieve']:
            return StadiumDetailSerializer

    def get_queryset(self):
        if self.request.user.role == RoleChoices.VENDOR:
            return Stadium.objects.filter(vendor=self.request.user)
        return Stadium.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return IsVendor(),
        return IsAuthenticated(),








