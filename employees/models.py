from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Employee(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        BLOCKED = 'blocked', 'Blocked'
        FINISHED = 'finished', 'Finished'

    name = models.CharField(max_length=255)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    stack = models.JSONField(default=list, blank=True)
    readiness_score = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    current_task = models.ForeignKey(
        'Task',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_for_employees',
    )
    mentor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='mentees',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Task(models.Model):
    class Status(models.TextChoices):
        TODO = 'todo', 'To Do'
        IN_PROGRESS = 'in_progress', 'In Progress'
        REVIEW = 'review', 'Review'
        DONE = 'done', 'Done'

    title = models.CharField(max_length=255)
    assignee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='tasks',
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.TODO,
    )
    deadline = models.DateTimeField(null=True, blank=True)
    subtasks = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Review(models.Model):
    class Result(models.TextChoices):
        READY = 'ready', 'Ready'
        NOT_READY = 'not_ready', 'Not Ready'
        REPEAT_SPRINT = 'repeat_sprint', 'Repeat Sprint'

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    criteria_scores = models.JSONField(default=dict, blank=True)
    feedback = models.TextField(blank=True)
    result = models.CharField(
        max_length=20,
        choices=Result.choices,
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='reviews_created',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Review for {self.employee.name} ({self.result})'
