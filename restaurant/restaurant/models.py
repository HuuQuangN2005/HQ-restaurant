from django.db import models
from uuid import uuid4

class UUIDBaseModel(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True, db_index=True, editable=False)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
