from django.db import models
from django.contrib.gis.db import models as geomodels

from core.utils.base_model import BaseModel


class Stadium(BaseModel):
    vendor = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE, related_name='stadiums')
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    contact = models.CharField(max_length=256)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    location = geomodels.PointField(geography=True, null=True)

    class Meta:
        db_table = 'stadium'

    @property
    def lon(self):
        return self.location.x

    @property
    def lat(self):
        return self.location.y






