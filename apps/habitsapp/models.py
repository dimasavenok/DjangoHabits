from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

from apps.mainapp.models import BaseModel

User = get_user_model()

class Habit(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='habits')
    place = models.CharField(max_length=255)
    time = models.TimeField(help_text='Время когда нужно напомнить')
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    related_habit = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='children')
    period_days = models.PositiveSmallIntegerField(default=1)
    reward = models.TimeField(null=True, blank=True)
    duration_seconds = models.PositiveSmallIntegerField(default=60)
    is_public = models.BooleanField(default=False)

    def clean(self):
        if self.reward and self.related_habit:
            raise ValidationError('Нельзя одновременный выбор связанной привычки и указания вознаграждения')
        if self.duration_seconds and self.duration_seconds > 120:
            raise ValidationError('Время выполнения должно быть не больше 120 секунд.')
        if (self.related_habit and self.related_habit.is_pleasant) or self.related_habit.id != self.id:
            raise ValidationError('В связанные привычки могут попадать только привычки с признаком приятной привычки.')
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError('У приятной привычки не может быть вознаграждения или связанной привычки.')
        if not (1 <= self.period_days <= 7):
            raise ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')

    def __str__(self):
        return f'{self.user} | {self.action} - {self.time}'

