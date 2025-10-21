from rest_framework import viewsets

from apps.habitsapp.permissions import IsOwnerOrReedOnly
from apps.habitsapp.serializers import HabitsSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitsSerializer
    permission_classes = IsOwnerOrReedOnly

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
