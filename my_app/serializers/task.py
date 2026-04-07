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
        "created_at"
    ]

# Задание 3: Использование вложенных сериализаторов
# Создайте сериализатор для TaskDetailSerializer,
# который включает вложенный сериализатор для полного отображения связанных подзадач (SubTask).
# Сериализатор должен показывать все подзадачи, связанные с данной задачей.
# Шаги для выполнения:
# Определите TaskDetailSerializer в файле serializers.py.
# Вложите SubTaskSerializer внутрь TaskDetailSerializer.


class TaskDetailSerializer(serializers.ModelSerializer):
    subtasks = SubTaskSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = [
        "title",
        "description",
        "status",
        "deadline",
        "subtasks"
    ]

# Задание 4: Валидация данных в сериализаторах
# Создайте TaskCreateSerializer и добавьте валидацию для поля deadline,
# чтобы дата не могла быть в прошлом. Если дата в прошлом, возвращайте ошибку валидации.
# Шаги для выполнения:
# Определите TaskCreateSerializer в файле serializers.py.
# Переопределите метод validate_deadline для проверки даты.


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