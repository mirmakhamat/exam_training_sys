from rest_framework import serializers
from .models import Product, Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'owner',
        )


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'title',
            'owner',
            'lessons',
        )
