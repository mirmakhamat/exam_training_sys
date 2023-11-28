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
    start_time = models.PositiveIntegerField()
    end_time = models.PositiveIntegerField()


class UserLesson(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    viewed_times = models.ManyToManyField(ViewedTime, blank=True)
    last_viewed_time = models.PositiveIntegerField(default=0)
    total_viewed_time = models.PositiveIntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def update_last_viewed_time(self, time):
        self.last_viewed_time = time
        self.save()

    def update_status(self):
        times = self.viewed_times.all()
        viewed_time_duration = 0
        for time in times:
            viewed_time_duration += (time.end_time - time.start_time)
        if viewed_time_duration >= self.lesson.duration * 0.8:
            self.status = True
        self.total_viewed_time = viewed_time_duration
        self.save()

    def update_viewed_time(self, start_time, end_time):
        times = self.viewed_times.all()
        for time in times:
            if time.start_time >= start_time and time.end_time <= end_time:
                time.start_time = start_time
                time.end_time = end_time
                time.save()
                return
            if time.start_time <= start_time and time.end_time >= start_time and time.end_time <= end_time:
                time.end_time = end_time
                time.save()
                return
            if time.start_time >= start_time and time.start_time <= end_time and time.end_time >= end_time:
                time.start_time = start_time
                time.save()
                return

        viewed_time = ViewedTime.objects.create(
            start_time=start_time, end_time=end_time)
        self.viewed_times.add(viewed_time)

    def __str__(self):
        return f"{self.user} - {self.lesson}"
