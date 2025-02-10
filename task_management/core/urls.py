from rest_framework.routers import DefaultRouter

from .views import UserViewSet, ProjectViewSet, CategoryViewSet, PriorityViewSet, TaskViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
router = DefaultRouter()

router.register(r'users', UserViewSet)

router.register(r'projects', ProjectViewSet)

router.register(r'categories', CategoryViewSet)

router.register(r'priorities', PriorityViewSet)

router.register(r'tasks', TaskViewSet)

urlpatterns = router.urls