from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from students.actions import validators
from students.models import Task, TaskConditional, User, Answer


class UpdateLesson(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = User.objects.get(pk=request.user.pk)
        for task in request.data.get('tasks'):
            task_id = task.get('task-id')
            answer = task.get('answer')
            task_obj = Task.objects.get(pk=task_id)
            lesson = task_obj
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
                    validators[task.type](answer=answer, user=user, lesson=lesson, true_answer=true_answer,
                                          task_conditional=task_conditional)
            return Response('Ваш ответ принят.')