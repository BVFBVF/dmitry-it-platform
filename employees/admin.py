from django.contrib import admin

from .models import Employee, Review, Task


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'readiness_score', 'mentor')
    list_filter = ('status',)
    search_fields = ('name',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assignee', 'status', 'deadline')
    list_filter = ('status',)
    search_fields = ('title',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'result', 'created_by', 'created_at')
    list_filter = ('result',)
    search_fields = ('employee__name', 'feedback')
