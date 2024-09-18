from rest_framework import serializers
from red_book_server.models.models import Category, RedBookItem, RedBookLocation


class RedBookLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedBookLocation
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class RedBookSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    location = RedBookLocationSerializer()
    class Meta:
        model = RedBookItem
        fields = '__all__'
