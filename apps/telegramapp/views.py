from django.shortcuts import render
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.telegramapp.models import TelegramUser, TelegramMessage
from apps.telegramapp.serializers import TelegramUserSerializer, TelegramUserCreateSerializer, TelegramMessageSerializer


class TelegramUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TelegramUserSerializer

    def get_object(self):
        telegram_user, created = TelegramUser.objects.get_or_create(
            user=self.request.user
        )
        return telegram_user


class TelegramUserCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TelegramUserCreateSerializer

    def perform_create(self, serializer):
        serializer.save()


class TelegramMessageListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = TelegramMessageSerializer

    def get_queryset(self):
        try:
            telegram_user = TelegramUser.objects.get(user=self.request.user)
            return TelegramMessage.objects.filter(user=telegram_user)
        except TelegramUser.DoesNotExist:
            return TelegramMessage.objects.none()


@extend_schema(
    request=TelegramUserCreateSerializer,
    responses={201: TelegramUserSerializer, 200: TelegramUserSerializer},
    examples=[
        OpenApiExample(
            'Пример запроса',
            value={
                "telegram_id": 123456789,
                "username": "my_telegram_username",
                "first_name": "Иван",
                "last_name": "Иванов"
            },
        )
    ],
    description="Создаёт или обновляет связь Telegram-пользователя с текущим аккаунтом."
)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def connect_telegram(request):
    """Подключение Telegram аккаунта"""
    telegram_id = request.data.get('telegram_id')
    username = request.data.get('username')
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')

    if not telegram_id:
        return Response(
            {'error': 'Telegram ID обязателен'},
            status=status.HTTP_400_BAD_REQUEST
        )

    telegram_user, created = TelegramUser.objects.get_or_create(
        user=request.user,
        defaults={
            'telegram_id': telegram_id,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
    )

    if not created:
        telegram_user.telegram_id = telegram_id
        telegram_user.username = username
        telegram_user.first_name = first_name
        telegram_user.last_name = last_name
        telegram_user.save()

    return Response({
        'message': 'Telegram аккаунт успешно подключен',
        'telegram_user': TelegramUserSerializer(telegram_user).data
    }, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def disconnect_telegram(request):
    """Отключение Telegram аккаунта"""
    try:
        telegram_user = TelegramUser.objects.get(user=request.user)
        telegram_user.delete()
        return Response(
            {'message': 'Telegram аккаунт отключен'},
            status=status.HTTP_200_OK
        )
    except TelegramUser.DoesNotExist:
        return Response(
            {'error': 'Telegram аккаунт не подключен'},
            status=status.HTTP_404_NOT_FOUND
        )