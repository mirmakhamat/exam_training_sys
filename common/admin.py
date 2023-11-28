from django.contrib import admin
from .models import Product, Lesson


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_to_video', 'duration')