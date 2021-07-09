from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from students.actions import validators
from students.models import Task, TaskConditional, User, Answer

from students.serializers import UserListSerializer, UserAllSerializer, UserTopSerializer, UserDetailSerializer, \
    LessonDetailSerializer


class UpdateLesson(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        for task in request.data.get('tasks'):
            task_id = task.get('task-id')
            answer = task.get('answer')
            task_obj = Task.objects.get(pk=task_id)
            true_answer = Answer.objects.get(task=task_obj, is_true=True)
            try:
                task_conditional = TaskConditional.objects.get(task=task_obj, user=request.user)
            except:
                task_conditional = TaskConditional.objects.create(task=task_obj, user=request.user)
            if task_conditional.status_task != True:
                if task.type == 'custom':
                    task_conditional.user_answer = answer
                    task_conditional.save()
                    return Response('Ваш ответ будет обработан модератером.')
                else:
                    validators[task.type](answer=answer, user=user, lesson=task_obj.lesson, true_answer=true_answer,
                                          task_conditional=task_conditional)
            return Response('Ваш ответ принят.')


class UserListView(ListAPIView):
    model = User

    def get_serializer_class(self):
        if self.request.GET.get('marksonly', None):
            return UserListSerializer
        return UserAllSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lesson_name'] = self.request.GET.get('lesson')
        return context

    def get_queryset(self):
        params = {
            field_name: value for field_name, value in self.request.GET.items()
        }
        if 'lesson' in params:
            del params['lesson']
        if 'top' in params:
            del params['top']
        if 'marksonly' in params:
            del params['marksonly']
        if self.request.GET.get('top', None):
            queryset = User.objects.filter(**params).order_by('-total_appraisal')[:int(self.request.GET.get('top'))]
        else:
            queryset = User.objects.filter(**params).order_by('-total_appraisal')
        return queryset


class UserTopListView(ListAPIView):
    model = User
    serializer_class = UserTopSerializer

    def get_queryset(self):
        if self.request.GET.get('n', None):
            queryset = User.objects.all().order_by('-total_appraisal')[:int(self.request.GET.get('n'))]
        else:
            queryset = User.objects.all().order_by('-total_appraisal')
        return queryset


class UserDetailView(APIView):
    model = User
    serializer_class = UserDetailSerializer

    def get(self, request):
        if request.GET.get('name', None):
            queryset = User.objects.get(username=request.GET.get('name'))
        elif request.GET.get('email', None):
            queryset = User.objects.get(email=request.GET.get('email'))
        seriazlier = UserDetailSerializer(queryset)
        return Response({'student': seriazlier.data})


class LessonDetailView(ListAPIView):
    model = User
    serializer_class = LessonDetailSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['lesson_name'] = self.request.GET.get('lesson')
        return context

    def get_queryset(self):
        params = {
            field_name: value for field_name, value in self.request.GET.items()
        }
        if 'lesson' in params:
            del params['lesson']

        if params:
            queryset = User.objects.filter(**params).order_by('-total_appraisal')
        else:
            queryset = User.objects.all().order_by('-total_appraisal')
        return queryset


def check_view(request):
    return render(request, 'index.html')


def email_user(request):
    if request.method == 'GET':
        email = request.GET['email']
        user = User.objects.get(email=email)
        task_conditional = TaskConditional.objects.filter(user=user)
        login(request, user)
        return render(request, 'account.html', {'student': user, 'tasks': task_conditional})


def user_logout(request):
    logout(request)
    return redirect('information')