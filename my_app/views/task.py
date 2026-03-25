from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

from django.db.models import Count
from datetime import datetime

from my_app.serializers import TaskSerializer
from my_app.models import Task


@api_view(["POST"])
def create_task(request: Request)-> Response:
    try:
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return Response(
            data=str(e),
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["GET"])
def get_all_tasks(request: Request)-> Response:
    queryset: QuerySet[Task] = Task.objects.all()
    serializer = TaskSerializer(queryset, many=True)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_task_by_id(request: Request, pk: int)-> Response:
    try:
        obj: Task = Task.objects.get(pk=pk)
    except Task.DoesNotExist as e:
        return Response(
            data=str(e),
            status=status.HTTP_404_NOT_FOUND
        )
    serializer = TaskSerializer(obj)
    return Response(
        data=serializer.data,
        status=status.HTTP_200_OK
    )

# Задание 3: Агрегирующий эндпоинт для статистики задач
# Создайте эндпоинт для получения статистики задач, таких как общее количество задач, количество задач по каждому статусу и количество просроченных задач.
# Шаги для выполнения:
# Определите представление для агрегирования данных о задачах.
# Создайте маршрут для обращения к представлению.
# Оформите ваш ответ следующим образом:
# Код эндпоинтов: Вставьте весь код представлений и маршрутов.

@api_view(["GET"])
def get_stat(request: Request)-> Response:
    task_count = Task.objects.all().count()

    # количество задач по каждому статусу
    status_count = Task.objects.values("status").annotate(count=Count('id'))

    # количество просроченных задач
    overdue_count = Task.objects.filter(deadline__lt=datetime.now()).count()

    return Response(
        data={
            'total_tasks': task_count,
            'tasks_by_status': {item['status']: item['count'] for item in status_count},
            'overdue_tasks': overdue_count
        }
        ,
        status=status.HTTP_200_OK
    )