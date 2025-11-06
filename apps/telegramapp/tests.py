from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.habitsapp.models import Habit
from apps.telegramapp.models import TelegramUser, TelegramMessage

User = get_user_model()


class TelegramUserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.telegram_user = TelegramUser.objects.create(
            user=self.user,
            telegram_id=123456789,
            username='my_telegram',
            first_name='Иван',
            last_name='Иванов'
        )

    def test_str_method(self):
        self.assertEqual(str(self.telegram_user), f"{self.user.username} ({self.telegram_user.telegram_id})")

    def test_create_telegram_user(self):
        self.assertEqual(TelegramUser.objects.count(), 1)
        self.assertEqual(self.telegram_user.telegram_id, 123456789)


class TelegramMessageModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser2', password='password')
        self.telegram_user = TelegramUser.objects.create(user=self.user, telegram_id=987654321)
        self.habit = Habit.objects.create(user=self.user, place="Home", time="12:00", action="Test habit")
        self.message = TelegramMessage.objects.create(
            user=self.telegram_user,
            habit=self.habit,
            message_text="Test message"
        )

    def test_is_sent_default(self):
        self.assertFalse(self.message.is_sent)

    def test_str_method(self):
        self.assertEqual(str(self.message.user), str(self.telegram_user))


class TelegramAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='password')
        self.client.force_authenticate(user=self.user)

    def test_connect_telegram_create(self):
        data = {
            "telegram_id": "111222333",
            "username": "api_telegram",
            "first_name": "Иван",
            "last_name": "Петров"
        }
        response = self.client.post('/api/telegram/telegram/connect/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TelegramUser.objects.count(), 1)
        self.assertEqual(TelegramUser.objects.get(user=self.user).telegram_id, 111222333)

    def test_connect_telegram_update(self):
        telegram_user = TelegramUser.objects.create(user=self.user, telegram_id=111222333)
        data = {
            "telegram_id": "444555666",
            "username": "updated_username",
            "first_name": "Петр",
            "last_name": "Сидоров"
        }
        response = self.client.post('/api/telegram/telegram/connect/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        telegram_user.refresh_from_db()
        self.assertEqual(telegram_user.telegram_id, 444555666)
        self.assertEqual(telegram_user.username, "updated_username")

    def test_disconnect_telegram(self):
        TelegramUser.objects.create(user=self.user, telegram_id=111222333)
        response = self.client.delete('/api/telegram/telegram/disconnect/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(TelegramUser.objects.count(), 0)

    def test_disconnect_nonexistent_telegram(self):
        response = self.client.delete('/api/telegram/telegram/disconnect/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TelegramMessageListAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='msguser', password='password')
        self.client.force_authenticate(user=self.user)
        self.telegram_user = TelegramUser.objects.create(user=self.user, telegram_id=123123123)
        self.habit = Habit.objects.create(user=self.user, place="Office", time="09:00", action="Work habit")
        self.message = TelegramMessage.objects.create(
            user=self.telegram_user,
            habit=self.habit,
            message_text="Hello"
        )

    def test_message_list(self):
        response = self.client.get('/api/telegram/telegram/messages/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['message_text'], "Hello")
