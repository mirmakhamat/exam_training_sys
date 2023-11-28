from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=120)
    link_to_video = models.URLField()
    duration = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=120)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson, related_name='products', blank=True)
    students = models.ManyToManyField('auth.User', related_name='products', blank=True)

    def __str__(self):
        return self.title


class ViewedTime(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class UserLesson(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    status = models.CharField(max_length=120)
    viewed_times = models.ManyToManyField(ViewedTime)

    def __str__(self):
        return f"{self.user} - {self.lesson}"
