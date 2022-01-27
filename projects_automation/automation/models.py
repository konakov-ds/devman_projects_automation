from django.db import models


class PM(models.Model):
    tg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    working_interval_from = models.TimeField(blank=True, null=True)
    working_interval_to = models.TimeField(blank=True, null=True)
    CHOICES = (
        ('blue', 'синий'),
        ('orange', 'оранжевый'),
        ('green', 'зеленый'),
        ('red', 'красный'),
        ('purple', 'фиолетовый'),
    )
    board_bg = models.CharField(
        verbose_name='Trello цвет',
        max_length=15,
        blank=True,
        null=True,
        choices=CHOICES,
        default='green'
        )

    def __str__(self):
        return f'PM {self.name}_{self.tg_id}'

    class Meta:
        verbose_name = 'Проджект менеджер'
        verbose_name_plural = 'Проджект менеджеры'
        ordering = ['working_interval_from']


class Group(models.Model):
    pm = models.ForeignKey(PM, related_name='groups', on_delete=models.CASCADE)
    start_from = models.DateTimeField(blank=True, null=True)
    board_url = models.URLField(verbose_name='URL Trello доски', blank=True, null=True)

    def __str__(self):
        return f'Group {self.id} under PM {self.pm.name}'

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'
        ordering = ['start_from']


class Student(models.Model):
    tg_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    group = models.ForeignKey(Group, related_name='students',
                              null=True, blank=True, on_delete=models.SET_NULL)
    level = models.CharField(max_length=20)
    working_interval_from = models.TimeField(blank=True, null=True)
    working_interval_to = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f'Student {self.name}_{self.tg_id}'

    class Meta:
        verbose_name = 'Ученик'
        verbose_name_plural = 'Ученики'
        ordering = ['level']
