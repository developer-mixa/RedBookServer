from django.db import models
from uuid import uuid4

class UUIDMixin(models.Model):
    """Class which adds id field."""

    id = models.UUIDField(primary_key=True, blank=True, editable=False, default=uuid4)

    class Meta:
        abstract = True