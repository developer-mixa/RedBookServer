from rest_framework import serializers
from red_book_server.models.models import Category, RedBookItem


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class RedBookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = RedBookItem
        fields = '__all__'
