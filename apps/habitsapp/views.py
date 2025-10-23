from rest_framework import viewsets, generics, permissions

from apps.habitsapp.models import Habit
from apps.habitsapp.permissions import IsOwnerOrReedOnly
from apps.habitsapp.serializers import HabitsSerializer, RegisterSerializer


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitsSerializer
    permission_classes = (IsOwnerOrReedOnly,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)