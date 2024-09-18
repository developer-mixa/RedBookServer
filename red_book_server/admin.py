from django.contrib import admin
from red_book_server.models.models import Category, RedBookItem, RedBookLocation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(RedBookItem)
class RedBookItemAdmin(admin.ModelAdmin):
    model = RedBookItem


@admin.register(RedBookLocation)
class RedBookLocation(admin.ModelAdmin):
    model = RedBookLocation