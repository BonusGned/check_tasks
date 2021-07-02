from django.contrib import admin

from students.models import User, Lesson, Task, TaskConditional, Answer


class TaskConditionalInline(admin.TabularInline):
    model = TaskConditional
    extra = 1


class AnswerInline(admin.TabularInline):
    model = Answer


class TaskInline(admin.TabularInline):
    model = Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = [TaskConditionalInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    inlines = [TaskInline]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
