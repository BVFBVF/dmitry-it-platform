from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmployeeViewSet, ReviewViewSet, TaskViewSet

router = DefaultRouter()
router.register('employees', EmployeeViewSet, basename='employee')
router.register('tasks', TaskViewSet, basename='task')
router.register('reviews', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
]
