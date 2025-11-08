from celery import shared_task
from django.conf import settings
from django.utils import timezone
from telegram import Bot

from apps.habitsapp.models import Habit
from apps.telegramapp.models import TelegramUser, TelegramMessage


@shared_task
def send_telegram_message(telegram_id, message_text, habit_id=None):
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        bot.send_message(chat_id=telegram_id, text=message_text)

        if habit_id:
            try:
                habit = Habit.objects.get(id=habit_id)
                telegram_user = TelegramUser.objects.get(telegram_id=telegram_id)
                TelegramMessage.objects.create(
                    user=telegram_user,
                    habit=habit,
                    message_text=message_text,
                    is_sent=True
                )
            except (Habit.DoesNotExist, TelegramUser.DoesNotExist):
               print('ERROR')

        return f"Сообщение отправлено пользователю {telegram_id}"
    except Exception as e:

        return f"Ошибка отправки сообщения: {e}"


@shared_task
def send_habit_reminders():
    current_time = timezone.now().time()
    current_date = timezone.now().date()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute,
        user__telegram_profile__is_active=True
    ).select_related('user__telegram_profile')

    for habit in habits:
        try:
            telegram_user = habit.user.telegram_profile

            today_messages = TelegramMessage.objects.filter(
                user=telegram_user,
                habit=habit,
                sent_at__date=current_date
            )

            if not today_messages.exists():
                message_text = f"⏰ Напоминание о привычке!\n\n"
                message_text += f"Действие: {habit.action}\n"
                message_text += f"Место: {habit.place}\n"
                message_text += f"Время: {habit.time.strftime('%H:%M')}\n"
                message_text += f"Время на выполнение: {habit.estimated_time} секунд\n"

                if habit.reward:
                    message_text += f"Вознаграждение: {habit.reward}\n"
                elif habit.related_habit:
                    message_text += f"Связанная привычка: {habit.related_habit.action}\n"

                send_telegram_message.delay(
                    telegram_user.telegram_id,
                    message_text,
                    habit.id
                )

        except Exception as e:
            print('ERROR')

