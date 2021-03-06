# Generated by Django 4.0.1 on 2022-01-27 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='board_url',
            field=models.URLField(blank=True, null=True, verbose_name='URL Trello доски'),
        ),
        migrations.AddField(
            model_name='pm',
            name='board_bg',
            field=models.CharField(blank=True, choices=[('blue', 'синий'), ('orange', 'оранжевый'), ('green', 'зеленый'), ('red', 'красный'), ('purple', 'фиолетовый')], default='green', max_length=15, null=True, verbose_name='Trello цвет'),
        ),
    ]
