from django.conf import settings
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from apps.habitsapp.models import Habit
from apps.telegramapp.models import TelegramUser


class HabitsBot:
    def __init__(self):
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()

    def setup_handlers(self):
        self.application.add_handler(CommandHandler('start', self.start_command))
        self.application.add_handler(CommandHandler('habits', self.habits_command))
        self.application.add_handler(CommandHandler('connect', self.connect_command))

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.effective_user
        user = TelegramUser.objects.filter(telegram_id=telegram_user.id).first()
        if user:
            welcome_text = f"Привет, {telegram_user.first_name or user.first_name}!\n\n"
            welcome_text += "Вы уже подключены к системе управления привычками.\n"
            welcome_text += "Используйте /habits для просмотра ваших привычек."
        else:
            welcome_text = f"Привет, {telegram_user.first_name}!\n\n"
            welcome_text += "Добро пожаловать в систему управления привычками!\n\n"
            welcome_text += "Для начала работы вам нужно подключить ваш аккаунт.\n"
            welcome_text += "Используйте команду /connect для получения инструкций."
        await update.message.reply_text(welcome_text)


    async def habits_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_user = update.effective_user
        user = TelegramUser.objects.filter(telegram_id=telegram_user.id).first()
        if user:
            habits = Habit.objects.filter(user=user)
            if habits.exists():
                message_text = "📋 Ваши привычки:\n\n"
                for habit in habits:
                    status_emoji = "✅" if habit.is_pleasant else "🎯"
                    message_text += f"{status_emoji} {habit.action}\n"
                    message_text += f" 📍 Место: {habit.place}\n"
                    message_text += f" ⏰ Время: {habit.time.strftime('%H:%M')}\n"
                    message_text += f" 📅 Периодичность: каждые {habit.period_days} дн.\n\n"
                await update.message.reply_text(message_text)
            else:
                await update.message.reply_text(
                    "У вас пока нет привычек.\n"
                    "Создайте их в веб-приложении!"
                )
        else:
            await update.message.reply_text(
                "Сначала подключите ваш аккаунт командой /connect"
            )

    async def connect_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /connect"""
        user = update.effective_user

        connect_text = f"""
🔗 Подключение аккаунта

Для подключения вашего Telegram аккаунта к системе управления привычками:

1. Зарегистрируйтесь или войдите в веб-приложение
2. В разделе "Telegram" введите ваш Telegram ID: {user.id}
3. Сохраните настройки

После этого вы будете получать напоминания о привычках!

🌐 Веб-приложение: [ссылка на ваше приложение]
        """
        await update.message.reply_text(connect_text)

    def run(self):
        self.application.run_polling()