from .seriliazers import ProductSerializer, ProductListSerializer, LessonSerializer, UserLessonSerializer
from .models import Product, UserLesson
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action


class StatsViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response({
            'total_students': User.objects.count(),
            'total_products': Product.objects.count(),
            'products': Product.objects.annotate(
                total_lessons=Sum('lessons__id')).values(
                    'id', 'title', 'total_lessons'),
            'lessons_watched_by_all_student': UserLesson.objects.filter(
                status=True).count(),
            'total_viewed_time': UserLesson.objects.aggregate(
                total_viewed_time=Sum('total_viewed_time'))['total_viewed_time'],
        })


class LessonViewSet(viewsets.ViewSet):
    @action(detail=True, methods=['POST'])
    def set_time(self, request, product_id=None, pk=None):
        start_time = request.data.get('start_time')
        end_time = request.data.get('end_time')

        if start_time is None or end_time is None:
            return Response({'message': 'Start time and end time are required'})

        product = get_object_or_404(Product, id=product_id)
        get_object_or_404(product.students.all(), id=request.user.id)

        lesson = get_object_or_404(product.lessons.all(), id=pk)
        user_lesson, _ = UserLesson.objects.get_or_create(
            user=request.user, lesson=lesson)
        user_lesson.update_viewed_time(start_time, end_time)
        user_lesson.update_status()
        user_lesson.update_last_viewed_time(end_time)
        return Response({'message': 'Viewed time updated successfully'})

    def list(self, request, product_id=None, pk=None):
        product = get_object_or_404(Product, id=product_id)
        get_object_or_404(product.students.all(), id=request.user.id)
        lessons = product.lessons.all()
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data)

    def retrieve(self, request, product_id=None, pk=None):
        product = get_object_or_404(Product, id=product_id)
        get_object_or_404(product.students.all(), id=request.user.id)
        lesson = get_object_or_404(product.lessons.all(), id=pk)
        user_lesson = get_object_or_404(
            UserLesson, lesson=lesson, user=request.user)

        serializer = UserLessonSerializer(user_lesson, many=False)
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
