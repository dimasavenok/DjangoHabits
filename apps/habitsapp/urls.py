from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.habitsapp.views import HabitViewSet, RegisterView, login_user, logout_user

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path("", include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', login_user, name='login'),
    path('auth/logout/', logout_user, name='logout'),
]