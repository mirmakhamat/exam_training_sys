from .seriliazers import ProductSerializer, ProductListSerializer, LessonSerializer
from .models import Product, Lesson
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class LessonViewSet(viewsets.ViewSet):
    def list(self, request, product_id=None):
        product = get_object_or_404(Product, id=product_id)
        get_object_or_404(product.students.all(), id=request.user.id)
        lessons = product.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def retrieve(self, request, product_id=None, pk=None):
        product = get_object_or_404(Product, id=product_id)
        lesson = get_object_or_404(product.lessons.all(), id=pk)
        serializer = LessonSerializer(lesson, many=False)
        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['POST'])
    def register(self, request, pk=None):
        product = Product.objects.get(id=pk)
        product.students.add(request.user)
        return Response({'message': 'User registered successfully'})

    def list(self, request):
        Products = Product.objects.all()
        serializer = ProductListSerializer(Products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if request.user.is_authenticated:
            product = Product.objects.get(id=pk)
            get_object_or_404(product.students.all(), id=request.user.id)
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        else:
            return Response({'message': 'User is not authenticated'})

