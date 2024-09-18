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


class RedBookLocation(UUIDMixin):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self) -> str:
        return f'lon:{self.longitude} lat:{self.latitude}'
    
    class Meta:
        db_table = '"location"'


class RedBookItem(UUIDMixin):
    name = models.TextField(unique=True, max_length=PARK_NAME_MAX_LEN, null=False, blank=False)
    description = models.TextField(unique=True, max_length=PARK_DESCRIPTION_MAX_LEN, null=False, blank=False)
    image_url = models.URLField(null=False, blank=False)
    count = models.IntegerField(null=False, blank=False, validators=[check_positive_number])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    location = models.ForeignKey(RedBookLocation, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        db_table = '"red_book_item"'
        unique_together = ('name', 'description',)


