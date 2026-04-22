# Задание 1: Реализация CRUD для категорий с использованием ModelViewSet
# Шаги для выполнения:
# Создайте CategoryViewSet, используя ModelViewSet для CRUD операций.
# Добавьте маршрут для CategoryViewSet.
# Добавьте кастомный метод count_tasks используя декоратор @action для подсчета количества задач, связанных с каждой категорией.
#

from urllib.request import Request

from django.core.serializers import serialize
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db.models import Count
from rest_framework.permissions import IsAdminUser

from my_app.models import Category
from my_app.serializers import CategoryCreateSerializer, CategoryCountSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action in {'list', 'count_tasks'}:
            return CategoryCountSerializer
        return CategoryCreateSerializer

    @action(methods=["GET"], detail=False)
    def count_tasks(self, request: Request) -> Response:
        queryset = self.get_queryset().annotate(task_count=Count('tasks'))
        serializer = self.get_serializer(queryset, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
