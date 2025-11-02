from django.db import models

from apps.habitsapp.models import Habit
from apps.mainapp.models import BaseModel
from apps.telegramapp.models.telegram_user import TelegramUser


class TelegramMessage(BaseModel):
    user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, related_name='telegram_profile')
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='habit')
    message_tex = models.TextField()
    is_send = models.BooleanField(default=False)
    
