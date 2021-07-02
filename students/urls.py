from django.contrib import admin
from django.urls import path

from students.views import UpdateLesson

urlpatterns = [
    path('lesson/', UpdateLesson.as_view()),
]
