from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from my_app.models import SubTask
from my_app.serializers import SubTaskSerializer
from my_app.serializers import SubTaskCreateSerializer
# Задание 2:
# Добавить пагинацию в отображение списка подзадач.
# На одну страницу должно отображаться не более 5 объектов.
# Отображение объектов должно идти в порядке убывания даты
# (от самого последнего добавленного объекта к самому первому)
# Задание 3:
# Добавить или обновить, если уже есть, эндпоинт на получение списка всех подзадач по названию главной задачи и статусу подзадач.
# Если фильтр параметры в запросе не передавались - выводить данные по умолчанию, с учётом пагинации.
# Если бы передан фильтр параметр названия главной задачи - выводить данные по этой главной задаче.
# Если был передан фильтр параметр конкретного статуса подзадачи - выводить данные по этому статусу.
# Если были переданы оба фильтра - выводить данные в соответствии с этими фильтрами.

# class SubTaskListAPIView(APIView, PageNumberPagination):
#     page_size = 5
#
#
#     def get_queryset(self):
#         queryset = SubTask.objects.all()
#
#         sort_order = self.request.query_params.get('sort', 'desc')
#         task_title = self.request.query_params.get('task_title')
#         status = self.request.query_params.get('status')
#
#         if sort_order == 'asc':
#             queryset = queryset.order_by('created_at')
#         else:
#             queryset = queryset.order_by('-created_at')
#
#         if task_title:
#             queryset = queryset.filter(task__title=task_title)
#
#         if status:
#             queryset = queryset.filter(status=status)
#
#         return queryset
#
#
#     def get_page_size(self, request: Request):
#         page_size = request.query_params.get('page_size')
#
#         if page_size and page_size.isdigit():
#             return int(page_size)
#         return self.page_size
#
#
#     def get(self, request: Request, *args, **kwargs) -> Response:
#         queryset = self.get_queryset()
#
#         page_size = self.get_page_size(request)
#         self.page_size = page_size
#
#         results = self.paginate_queryset(
#             queryset=queryset,
#             request=request,
#             view=self
#         )
#
#         serializer = SubTaskSerializer(results, many=True)
#
#         return self.get_paginated_response(
#             data=serializer.data,
#         )
#
#
#     def post(self, request: Request, *args, **kwargs) -> Response:
#         serializer = SubTaskCreateSerializer(
#             data=request.data
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#
#         return Response(
#             data=serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#
# class SubTaskDetailUpdateDeleteView(APIView):
#
#     def get_object(self):
#         try:
#             subtasks = SubTask.objects.get(pk=self.kwargs['pk'])
#         except SubTask.DoesNotExist:
#             raise NotFound('Подзадача не найдена')
#         return subtasks
#
#
#     def get(self, request: Request, pk) -> Response:
#         subtasks = self.get_object()
#
#         serializer = SubTaskSerializer(subtasks)
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def put(self, request: Request, pk) -> Response:
#         subtasks = self.get_object()
#
#         serializer = SubTaskCreateSerializer(subtasks, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )
#
#         return Response(
#             data=serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )
#
#     def delete(self, request: Request, pk) -> Response:
#         subtasks = self.get_object()
#
#         subtasks.delete()
#
#         return Response(
#             status=status.HTTP_204_NO_CONTENT
#         )

# ----------------------------------------------------------------------------------------------------------------------
# Задание 2: Замена представлений для подзадач (SubTasks) на Generic Views
# Шаги для выполнения:
# Замените классы представлений для подзадач на Generic Views:
# Используйте ListCreateAPIView для создания и получения списка подзадач.
# Используйте RetrieveUpdateDestroyAPIView для получения, обновления и удаления подзадач.
# Реализуйте фильтрацию, поиск и сортировку:
# Реализуйте фильтрацию по полям status и deadline.
# Реализуйте поиск по полям title и description.
# Добавьте сортировку по полю created_at.

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.db.models import Q


class SubTaskListCreateGenericView(ListCreateAPIView):

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.query_params.get('status')
        deadline = self.request.query_params.get('deadline')
        search = self.request.query_params.get('search')
        ordering = self.request.query_params.get('ordering', '-created_at')
        task_title = self.request.query_params.get('task_title')


        if status:
            queryset = queryset.filter(status=status)

        if deadline:
            queryset = queryset.filter(deadline__date=deadline)

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        if ordering:
            queryset = queryset.order_by(ordering)

        if task_title:
            queryset = queryset.filter(task__title=task_title)

        return queryset


class SubTaskDetailGenericView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer