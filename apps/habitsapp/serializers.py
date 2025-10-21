from rest_framework.exceptions import NotAuthenticated
from rest_framework import serializers

from apps.habitsapp.models import Habit


class HabitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.get('user') and request.user.is_authenticated:
            user = request.user
            habit = Habit.objects.create(
                user=user,
                **validated_data
            )
            habit.save()
            return habit
        raise NotAuthenticated('Пользователь не авторизован')

