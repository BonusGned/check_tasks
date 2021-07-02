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