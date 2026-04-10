# Задание 2: Переопределение методов create и update
# Создайте сериализатор для категории CategoryCreateSerializer,
# переопределив методы create и update для проверки уникальности названия категории.
# Если категория с таким названием уже существует, возвращайте ошибку валидации.
# Шаги для выполнения:
# Определите CategoryCreateSerializer в файле serializers.py.
# Переопределите метод create для проверки уникальности названия категории.
# Переопределите метод update для аналогичной проверки при обновлении.

from typing import Any
from rest_framework import serializers
from my_app.models import Category


class CategoryCountSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(
        required=False,
        read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'task_count', 'is_deleted']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


    def create(self, validated_data: dict[str, Any]) -> Category:
        name_category = Category.objects.filter(
            name__iexact=validated_data['name']).exists()
        if name_category:
            raise serializers.ValidationError(
                "Такая категория уже существует")
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data) -> Category:
        name_category = Category.objects.filter(
            name__iexact=validated_data['name']
        ).exclude(id=instance.id).exists()
        if name_category:
            raise serializers.ValidationError(
                "Такая категория уже существует"
            )

        # instance.name = validated_data['name']
        # instance.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance