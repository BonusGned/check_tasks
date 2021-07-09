from django.contrib import admin
from django.urls import path

from students.views import UpdateLesson, check_view, email_user, user_logout, UserListView, UserTopListView, \
    UserDetailView, LessonDetailView, sync

urlpatterns = [
    path('lesson/', UpdateLesson.as_view()),
    path('inf/', check_view, name='information'),
    path('email_information', email_user, name='email_user'),
    path('logout/', user_logout, name='logout'),
    path('api/v1/all', UserListView.as_view(), name='list_students'),
    path('api/v1/top', UserTopListView.as_view(), name='top_students'),
    path('api/v1/student', UserDetailView.as_view(), name='student'),
    path('api/v1/lesson', LessonDetailView.as_view(), name='lesson'),
    path('sync/', sync)
]
