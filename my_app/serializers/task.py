from rest_framework import serializers

from my_app.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
        "title",
        "description",
        "status",
        "deadline"
    ]