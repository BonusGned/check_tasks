
from django.contrib.auth.models import AbstractUser
from django.db import models

from students.managers import CustomUserManager


class User(AbstractUser):
    username = None
    email = models.EmailField('Email address', unique=True, blank=True)
    total_appraisal = models.FloatField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Lesson(models.Model):
    order_number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=2048)
    appraisal = models.FloatField(default=0)
    description = models.CharField(max_length=2048)

    def __str__(self):
        return f'{self.order_number}'


class TaskConditional(models.Model):
    user = models.ForeignKey('User', related_name='task_conditionals', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey('Task', related_name='tasks', on_delete=models.CASCADE)
    appraisal = models.FloatField(default=0)
    pessimizing_factor = models.FloatField(default=0)
    status_task = models.BooleanField(default=False)
    user_answer = models.CharField(max_length=2048, blank=True, null=True)


    def __str__(self):
        return f'{self.user}'


class Task(models.Model):
    TYPE_TASK_CHOICES = [
        ('number', 'number'),
        ('string', 'string'),
        ('range', 'range'),
        ('custom', 'custom'),
    ]

    order_number = models.PositiveSmallIntegerField()
    question = models.CharField(max_length=2048)
    lesson = models.ForeignKey('Lesson', related_name='lesson', on_delete=models.CASCADE)
    type = models.CharField(max_length=40, choices=TYPE_TASK_CHOICES)

    def __str__(self):
        return f'{self.order_number}'


class Answer(models.Model):
    is_true = models.BooleanField(default=False)
    answer_content = models.CharField(max_length=2048, default=0)
    from_range = models.FloatField(default=0)
    to_range = models.FloatField(default=0)
    task = models.ForeignKey('Task', related_name='answers', on_delete=models.CASCADE)
