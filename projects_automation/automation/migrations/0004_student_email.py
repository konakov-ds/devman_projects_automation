# Generated by Django 4.0.1 on 2022-01-28 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0003_alter_student_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
    ]
