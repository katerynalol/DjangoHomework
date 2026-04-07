from django.db.models import QuerySet
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Count
from datetime import datetime
from rest_framework.pagination import PageNumberPagination

from my_app.serializers import TaskSerializer
from my_app.models import Task


# Задание 1:
# Написать, или обновить, если уже есть, эндпоинт на получение списка всех задач по дню недели.
# Если никакой параметр запроса не передавался - по умолчанию выводить все записи.
# Если был передан день недели (например вторник) - выводить список задач только на этот день недели.


class TaskListAPIView(APIView, PageNumberPagination):
    page_size = 5

    DAY_MAPPING = {
        'понедельник': 2,
        'вторник': 3,
        'среда': 4,
        'четверг': 5,
        'пятница': 6,
        'суббота': 7,
        'воскресенье': 1
    }

    def get_queryset(self):
        queryset: QuerySet[Task] = Task.objects.all()

        weekday = self.request.query_params.get('day')

        if weekday:
            weekday_num = self.DAY_MAPPING.get(weekday.lower())
            if weekday_num:
                queryset = queryset.filter(deadline__week_day=weekday_num)

        return queryset


    def get_page_size(self, request: Request):
        page_size = request.query_params.get('page_size')

        if page_size and page_size.isdigit():
            return int(page_size)
        return self.page_size


    def get(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset()

        page_size = self.get_page_size(request)
        self.page_size = page_size

        results = self.paginate_queryset(
            queryset=queryset,
            request=request,
            view=self
        )

        serializer = TaskSerializer(results, many=True)

        return self.get_paginated_response(
            data=serializer.data,
        )


    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = TaskSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# @api_view(["POST"])
# def create_task(request: Request)-> Response:
#     try:
#         serializer = TaskSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_201_CREATED
#         )
#     except Exception as e:
#         return Response(
#             data=str(e),
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#
# @api_view(["GET"])
# def get_all_tasks(request: Request)-> Response:
#     queryset: QuerySet[Task] = Task.objects.all()
#     serializer = TaskSerializer(queryset, many=True)
#     return Response(
#         data=serializer.data,
#         status=status.HTTP_200_OK
#     )


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