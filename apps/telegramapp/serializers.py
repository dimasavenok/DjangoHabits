from django.contrib.auth import get_user_model
from rest_framework import serializers

from apps.habitsapp.models import Habit
from apps.telegramapp.models import TelegramUser, TelegramMessage

User = get_user_model()

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class HabitShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ['id', 'action', 'time']

class TelegramUserSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)

    class Meta:
        model = TelegramUser
        fields = [
            'id',
            'user',
            'telegram_id',
            'username',
            'first_name',
            'last_name',
            'is_active',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'telegram_id': {'help_text': 'Уникальный идентификатор пользователя в Telegram'},
            'username': {'help_text': 'Имя пользователя в Telegram (без @)'},
            'first_name': {'help_text': 'Имя из профиля Telegram'},
            'last_name': {'help_text': 'Фамилия из профиля Telegram'},
            'is_active': {'help_text': 'Флаг активности связи с Telegram'},
        }

class TelegramMessageSerializer(serializers.ModelSerializer):
    user = TelegramUserSerializer(read_only=True)
    habit = HabitShortSerializer(read_only=True)

    class Meta:
        model = TelegramMessage
        fields = [
            'id',
            'user',
            'habit',
            'message_text',
            'is_sent',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {
            'message_text': {'help_text': 'Текст отправленного или запланированного сообщения'},
            'is_sent': {'help_text': 'Отправлено ли сообщение пользователю'},
        }


class TelegramUserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = ['telegram_id', 'username', 'first_name', 'last_name']
        extra_kwargs = {
            'telegram_id': {'help_text': 'Уникальный Telegram ID (обязателен)'},
            'username': {'help_text': 'Имя пользователя (без @)'},
            'first_name': {'help_text': 'Имя из Telegram'},
            'last_name': {'help_text': 'Фамилия из Telegram'},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        telegram_user, created = TelegramUser.objects.get_or_create(
            user=user,
            defaults=validated_data
        )
        if not created:
            for key, value in validated_data.items():
                setattr(telegram_user, key, value)
            telegram_user.save()
        return telegram_user