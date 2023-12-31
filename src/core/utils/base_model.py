from django.db import models


class BaseModel(models.Model):
    """ Custom Base Model """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """ Meta class """
        abstract = True
