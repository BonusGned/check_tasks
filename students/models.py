from django.contrib.auth.models import AbstractUser
from django.db import models

from students.managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField('Имя и Фамилия', max_length=40)
    email = models.EmailField('Email адрес', unique=True, blank=True)
    total_appraisal = models.FloatField('Итоговая оценка', default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    def get_all_appraisal_by_lessons(self, lesson_name=None):
        lesson_appraisal = []
        if not lesson_name:
            for lesson in Lesson.objects.all():
                for task in lesson.tasks.all():
                    sum_less, created = TaskConditional.objects.get_or_create(user=self, task=task)
                    lesson_appraisal.append(sum_less.appraisal)
            return sum(lesson_appraisal)
        for task in Lesson.objects.get(title=lesson_name).tasks.all():
            sum_less, created = TaskConditional.objects.get_or_create(user=self, task=task)
            lesson_appraisal.append(sum_less.appraisal)
        return sum(lesson_appraisal)

    def get_all_pessimizing_factor_by_lessons(self, lesson_name=None):
        lesson_pessimizing_factor = []
        if not lesson_name:
            for lesson in Lesson.objects.all():
                for task in lesson.tasks.all():
                    sum_less, created = TaskConditional.objects.get_or_create(user=self, task=task)
                    lesson_pessimizing_factor.append(sum_less.pessimizing_factor)
            return sum(lesson_pessimizing_factor)
        for task in Lesson.objects.get(title=lesson_name).tasks.all():
            sum_less, created = TaskConditional.objects.get_or_create(user=self, task=task)
            lesson_pessimizing_factor.append(sum_less.pessimizing_factor)
        return sum(lesson_pessimizing_factor)

    def get_all_user_answer_by_lessons(self, lesson_name=None):
        user_answer_list = []
        if not lesson_name:
            return None
        for task in Lesson.objects.get(title=lesson_name).tasks.all():
            sum_less, created = TaskConditional.objects.get_or_create(user=self, task=task)
            user_answer_list.append(sum_less.user_answer)
        return user_answer_list

    def get_all_status_task_by_lessons(self, lesson_name=None):
        status_task_list = []
        if not lesson_name:
            return None
        for task in Lesson.objects.get(title=lesson_name).tasks.all():
            sum_less, created = TaskConditional.objects.get_or_create(user=self, task=task)
            status_task_list.append(sum_less.status_task)
        return status_task_list


class Lesson(models.Model):
    order_number = models.PositiveSmallIntegerField('Номер урока')
    title = models.CharField('Название урока', max_length=124)
    description = models.CharField('Описание урока', max_length=2048)

    def __str__(self):
        return f'{self.order_number}'


class TaskConditional(models.Model):
    user = models.ForeignKey('User', related_name='task_conditionals', on_delete=models.CASCADE, null=True)
    task = models.ForeignKey('Task', related_name='tasks_conds', on_delete=models.CASCADE)
    appraisal = models.FloatField('Оценка за урок', default=0)
    pessimizing_factor = models.FloatField('Пессимизирующий фактор', default=0)
    status_task = models.BooleanField('Сдача задания', default=False)
    user_answer = models.CharField('Ответ студента', max_length=2048, blank=True, null=True)

    def __str__(self):
        return f'{self.user}'


class Task(models.Model):
    TYPE_TASK_CHOICES = [
        ('number', 'number'),
        ('string', 'string'),
        ('range', 'range'),
        ('custom', 'custom'),
    ]

    order_number = models.PositiveSmallIntegerField('Номер задания')
    question = models.CharField('Вопрос задания', max_length=2048)
    lesson = models.ForeignKey('Lesson', related_name='tasks', on_delete=models.CASCADE)
    type = models.CharField('Тип ответа', max_length=40, choices=TYPE_TASK_CHOICES)

    def __str__(self):
        return f'{self.order_number}'


class Answer(models.Model):
    is_true = models.BooleanField('Верный ответ', default=False)
    answer_content = models.CharField('Содержание ответа', max_length=2048, default=0)
    from_range = models.FloatField('Начало диапазона', default=0)
    to_range = models.FloatField('Конец диапазона', default=0)
    task = models.ForeignKey('Task', related_name='answers', on_delete=models.CASCADE)
