from django.db import models
from red_book_server.models.mixnins import UUIDMixin
from red_book_server.models.config import PARK_NAME_MAX_LEN, PARK_DESCRIPTION_MAX_LEN, MAX_CATEGORY_NAME
from red_book_server.models.validators import check_positive_number


class Category(UUIDMixin):
    name = models.TextField(unique=True, max_length=MAX_CATEGORY_NAME)

    def __str__(self) -> str:
        return self.name

    class Meta:
        db_table = '"category"'

class RedBookItem(UUIDMixin):
    name = models.TextField(unique=True, max_length=PARK_NAME_MAX_LEN, null=False, blank=False)
    description = models.TextField(unique=True, max_length=PARK_DESCRIPTION_MAX_LEN, null=False, blank=False)
    image_url = models.URLField(null=False, blank=False)
    count = models.IntegerField(null=False, blank=False, validators=[check_positive_number])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = '"red_book_item"'
        unique_together = ('name', 'description',)
