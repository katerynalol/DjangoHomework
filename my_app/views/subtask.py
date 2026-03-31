from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from my_app.models import SubTask
from my_app.serializers import SubTaskSerializer
from my_app.serializers import SubTaskCreateSerializer
# Задание 5: Создание классов представлений
# Создайте классы представлений для работы с подзадачами (SubTasks),
# включая создание, получение, обновление и удаление подзадач.
# Используйте классы представлений (APIView) для реализации этого функционала.
# Шаги для выполнения:
# Создайте классы представлений для создания и получения списка подзадач (SubTaskListCreateView).
# Создайте классы представлений для получения, обновления и удаления подзадач (SubTaskDetailUpdateDeleteView).
# Добавьте маршруты в файле urls.py, чтобы использовать эти классы.


class SubTaskListCreateView(APIView):

    def get(self, request: Request, *args, **kwargs) -> Response:
        subtasks = SubTask.objects.all()

        serializer = SubTaskSerializer(subtasks, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = SubTaskCreateSerializer(
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


class SubTaskDetailUpdateDeleteView(APIView):

    def get_object(self):
        try:
            subtasks = SubTask.objects.get(pk=self.kwargs['pk'])
        except SubTask.DoesNotExist:
            raise NotFound('Подзадача не найдена')
        return subtasks


    def get(self, request: Request, pk) -> Response:
        subtasks = self.get_object()

        serializer = SubTaskSerializer(subtasks)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, pk) -> Response:
        subtasks = self.get_object()

        serializer = SubTaskCreateSerializer(subtasks, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, pk) -> Response:
        subtasks = self.get_object()

        subtasks.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )