# from djoser.serializers import UserCreateSerializer
#
# from students.models import User
#
#
# class UserRegistrationSerializer(UserCreateSerializer):
#     def validate(self, attrs):
#         user = User(**attrs)
#         return attrs
#
#     class Meta(UserCreateSerializer.Meta):
#         fields = ('email', 'first_name', 'last_name')
from rest_framework import serializers

from students.models import User


class UserListSerializer(serializers.ModelSerializer):
    lesson_appraisal = serializers.SerializerMethodField('get_all_appraisal_by_lessons')

    def get_all_appraisal_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        lesson_appraisal = obj.get_all_appraisal_by_lessons(lesson_name=lesson_name)
        return lesson_appraisal

    class Meta:
        model = User
        fields = ('username', 'email', 'lesson_appraisal', 'total_appraisal')


class UserAllSerializer(serializers.ModelSerializer):
    lesson_appraisal = serializers.SerializerMethodField('get_all_appraisal_by_lessons')
    lesson_pessimizing_factor = serializers.SerializerMethodField('get_all_pessimizing_factor_by_lessons')

    class Meta:
        model = User
        fields = ('username', 'email', 'lesson_appraisal', 'total_appraisal', 'lesson_pessimizing_factor')

    def get_all_appraisal_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        lesson_appraisal = obj.get_all_appraisal_by_lessons(lesson_name=lesson_name)
        return lesson_appraisal

    def get_all_pessimizing_factor_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        lesson_pessimizing_factor = obj.get_all_pessimizing_factor_by_lessons(lesson_name=lesson_name)
        return lesson_pessimizing_factor


class UserTopSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'total_appraisal')


class UserDetailSerializer(serializers.ModelSerializer):
    lesson_appraisal = serializers.SerializerMethodField('get_all_appraisal_by_lessons')

    def get_all_appraisal_by_lessons(self, obj):
        lesson_appraisal = obj.get_all_appraisal_by_lessons(lesson_name=None)
        return lesson_appraisal

    class Meta:
        model = User
        fields = ('username', 'email', 'lesson_appraisal', 'total_appraisal')


class LessonDetailSerializer(serializers.ModelSerializer):
    lesson_appraisal = serializers.SerializerMethodField('get_all_appraisal_by_lessons')
    lesson_pessimizing_factor = serializers.SerializerMethodField('get_all_pessimizing_factor_by_lessons')
    list_status_task = serializers.SerializerMethodField('get_all_user_answer_by_lessons')
    list_user_answer = serializers.SerializerMethodField('get_all_status_task_by_lessons')

    class Meta:
        model = User
        fields = ('username', 'email', 'lesson_appraisal', 'total_appraisal', 'lesson_pessimizing_factor', 'list_status_task', 'list_user_answer')

    def get_all_appraisal_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        print(lesson_name)
        lesson_appraisal = obj.get_all_appraisal_by_lessons(lesson_name=lesson_name)
        return lesson_appraisal

    def get_all_pessimizing_factor_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        lesson_pessimizing_factor = obj.get_all_pessimizing_factor_by_lessons(lesson_name=lesson_name)
        return lesson_pessimizing_factor

    def get_all_user_answer_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        list_user_answer = obj.get_all_user_answer_by_lessons(lesson_name=lesson_name)
        return list_user_answer

    def get_all_status_task_by_lessons(self, obj):
        lesson_name = self.context.get('lesson_name')
        list_status_task = obj.get_all_status_task_by_lessons(lesson_name=lesson_name)
        return list_status_task
