from rest_framework import serializers

from .models import Employee, Review, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'id',
            'title',
            'assignee',
            'status',
            'deadline',
            'subtasks',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')


class ReviewSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(
        source='created_by.username',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'employee',
            'criteria_scores',
            'feedback',
            'result',
            'created_by',
            'created_by_username',
            'created_at',
        )
        read_only_fields = ('created_by', 'created_by_username', 'created_at')


class EmployeeListSerializer(serializers.ModelSerializer):
    mentor_username = serializers.CharField(
        source='mentor.username',
        read_only=True,
        default=None,
    )
    current_task_title = serializers.CharField(
        source='current_task.title',
        read_only=True,
        default=None,
    )

    class Meta:
        model = Employee
        fields = (
            'id',
            'name',
            'avatar',
            'status',
            'stack',
            'readiness_score',
            'current_task',
            'current_task_title',
            'mentor',
            'mentor_username',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('created_at', 'updated_at')


class EmployeeDetailSerializer(EmployeeListSerializer):
    tasks = TaskSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta(EmployeeListSerializer.Meta):
        fields = EmployeeListSerializer.Meta.fields + ('tasks', 'reviews')


class EmployeeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = (
            'name',
            'avatar',
            'status',
            'stack',
            'readiness_score',
            'current_task',
            'mentor',
        )

    def validate_stack(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError('stack must be a list of strings.')
        if not all(isinstance(item, str) for item in value):
            raise serializers.ValidationError('Each stack item must be a string.')
        return value

    def validate_readiness_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('readiness_score must be between 0 and 100.')
        return value

    def validate_current_task(self, value):
        if value is None:
            return value
        employee = self.instance
        if employee and value.assignee_id != employee.id:
            raise serializers.ValidationError(
                'current_task must belong to this employee.'
            )
        return value


class EmployeePartialUpdateSerializer(serializers.ModelSerializer):
    """PATCH: only status and readiness_score."""

    class Meta:
        model = Employee
        fields = ('status', 'readiness_score')

    def validate_readiness_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError('readiness_score must be between 0 and 100.')
        return value
