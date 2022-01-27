# Generated by Django 4.0.1 on 2022-01-27 10:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_from', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Команда',
                'verbose_name_plural': 'Команды',
                'ordering': ['start_from'],
            },
        ),
        migrations.CreateModel(
            name='PM',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(unique=True)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('working_interval_from', models.TimeField(blank=True, null=True)),
                ('working_interval_to', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Проджект менеджер',
                'verbose_name_plural': 'Проджект менеджеры',
                'ordering': ['working_interval_from'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tg_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=20)),
                ('working_interval_from', models.TimeField(blank=True, null=True)),
                ('working_interval_to', models.TimeField(blank=True, null=True)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='automation.group')),
            ],
            options={
                'verbose_name': 'Ученик',
                'verbose_name_plural': 'Ученики',
                'ordering': ['level'],
            },
        ),
        migrations.AddField(
            model_name='group',
            name='pm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='automation.pm'),
        ),
    ]
