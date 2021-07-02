import re

from rest_framework.response import Response


def string_valid(answer, user, lesson, true_answer, task_conditional):
    if answer.lower() == true_answer.answer_content.lower():
        task_conditional.appraisal = 1.0 - task_conditional.pessimizing_factor
        task_conditional.status_task = True
        lesson.appraisal += task_conditional.appraisal
        user.total_appraisal += task_conditional.appraisal
        task_conditional.save()
    else:
        task_conditional.pessimizing_factor += 0.25 if task_conditional.pessimizing_factor < 1.1 else 0
        task_conditional.save()
        return Response('Ваш ответ не является верным!')


def number_valid(answer, user, lesson, true_answer, task_conditional):
    answer = re.sub(',', ".", answer)
    answer = re.sub('[^0-9.]', '', answer)
    if float(answer) == true_answer.answer_content:
        task_conditional.appraisal = 1 - task_conditional.pessimizing_factor
        task_conditional.status_task = True
        lesson.appraisal += task_conditional.appraisal
        user.total_appraisal += task_conditional.appraisal
        task_conditional.save()
    else:
        task_conditional.pessimizing_factor += 0.25 if task_conditional.pessimizing_factor < 1.1 else 0
        task_conditional.save()
        return Response('Ваш ответ не является верным!')


def range_valid(answer, user, lesson, true_answer, task_conditional):
    answer = re.sub(',', ".", answer)
    answer = re.sub('[^0-9-]', '', answer)
    if true_answer.from_range >= float(answer) >= true_answer.to_range:
        task_conditional.appraisal = 1.0 - task_conditional.pessimizing_factor
        task_conditional.status_task = True
        lesson.appraisal += task_conditional.appraisal
        user.total_appraisal += task_conditional.appraisal
        task_conditional.save()
    else:
        task_conditional.pessimizing_factor += 0.25 if task_conditional.pessimizing_factor < 1.1 else 0
        task_conditional.save()
        return Response('Ваш ответ не является верным!')


validators = {
    'string': string_valid,
    'number': number_valid,
    'range': range_valid
}
