# Generated by Django 3.2.4 on 2021-06-30 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0008_task_user_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user_answer',
        ),
        migrations.AddField(
            model_name='taskconditional',
            name='user_answer',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
