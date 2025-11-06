from django.urls import path

from apps.telegramapp.views import TelegramMessageListView, TelegramUserView, connect_telegram, disconnect_telegram

urlpatterns = [
    path('telegram/user/', TelegramUserView.as_view(), name='telegram-user'),
    path('telegram/connect/', connect_telegram, name='telegram-connect'),
    path('telegram/disconnect/', disconnect_telegram, name='telegram-disconnect'),
    path('telegram/messages/', TelegramMessageListView.as_view(), name='telegram-messages'),
]