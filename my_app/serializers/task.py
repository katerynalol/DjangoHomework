from rest_framework import serializers
from django.utils import timezone
from my_app.models import Task
from my_app.serializers.subtask import SubTaskSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
        "title",
        "description",
        "status",
        "deadline",
        "created_at",
        "owner"
    ]


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
        "title",
        "description",
        "status",
        "deadline",
        "subtasks",
        "owner"
    ]


class TaskCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
        "title",
        "description",
        "status",
        "deadline"
    ]
    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Дата не может быть в прошлом")
        return value