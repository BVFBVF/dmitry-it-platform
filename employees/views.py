from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser

from accounts.permissions import EmployeePermission, ReviewPermission

from .models import Employee, Review, Task
from .serializers import (
    EmployeeCreateUpdateSerializer,
    EmployeeDetailSerializer,
    EmployeeListSerializer,
    EmployeePartialUpdateSerializer,
    ReviewSerializer,
    TaskSerializer,
)


class EmployeeFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=Employee.Status.choices)

    class Meta:
        model = Employee
        fields = ('status',)


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related(
        'mentor', 'current_task'
    ).prefetch_related('tasks', 'reviews')
    permission_classes = (EmployeePermission,)
    filterset_class = EmployeeFilter
    search_fields = ('name',)
    ordering_fields = ('name', 'readiness_score', 'created_at')
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return EmployeeDetailSerializer
        if self.action == 'create':
            return EmployeeCreateUpdateSerializer
        if self.action == 'partial_update':
            return EmployeePartialUpdateSerializer
        return EmployeeListSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related('assignee')
    serializer_class = TaskSerializer
    permission_classes = (EmployeePermission,)
    filterset_fields = ('status', 'assignee')
    search_fields = ('title',)
    ordering_fields = ('deadline', 'created_at')


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related('employee', 'created_by')
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)
    filterset_fields = ('result', 'employee')
    ordering_fields = ('created_at',)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ('update', 'partial_update', 'destroy'):
            from accounts.permissions import IsAdmin
            return [IsAdmin()]
        return super().get_permissions()
