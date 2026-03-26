# Задание 1: Переопределение полей сериализатора
# Создайте SubTaskCreateSerializer, в котором поле created_at будет доступно только для чтения (read_only).
# Шаги для выполнения:
# Определите SubTaskCreateSerializer в файле serializers.py.
# Переопределите поле created_at как read_only.

from rest_framework import serializers
from my_app.models import SubTask

class SubTaskCreateSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(
        read_only=True
    )
    class Meta:
        model = SubTask
        fields = '__all__'