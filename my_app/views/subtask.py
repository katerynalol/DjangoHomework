from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from my_app.permissions import IsOwner
from my_app.models import SubTask
from my_app.serializers import SubTaskSerializer
from my_app.serializers import SubTaskCreateSerializer


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


from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from django.db.models import Q


class SubTaskListCreateGenericView(ListCreateAPIView):

    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data["owner"] = self.request.user
        serializer.save()

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
    permission_classes = [IsOwner]


class MySubTaskListView(ListAPIView):
    serializer_class = SubTaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubTask.objects.filter(owner=self.request.user)