from django.contrib import admin
from red_book_server.models.models import Category, RedBookItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(RedBookItem)
class RedBookItemAdmin(admin.ModelAdmin):
    model = RedBookItem
