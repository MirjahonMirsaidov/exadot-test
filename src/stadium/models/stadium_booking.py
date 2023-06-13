from django.db import models

from core.utils.base_model import BaseModel


class StadiumBooking(BaseModel):
    stadium = models.ForeignKey('stadium.Stadium', on_delete=models.CASCADE, related_name='stadium_booking')
    user = models.ForeignKey('userprofile.UserProfile', on_delete=models.CASCADE, related_name='stadium_booking')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    class Meta:
        db_table = 'stadium_booking'






