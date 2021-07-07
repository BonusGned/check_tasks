from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):

    # Creat User
    def create_user(self, username, email, password, **kwargs):
        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(username=username, email=self.normalize_email(email))

        user.set_password(password)

        user.save()
        return user

    # Create SuperUser
    def create_superuser(self, username, email, password, **kwargs):
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(
            useranme=username, email=email, password=password
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user