"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)

from my_app.views.task import (TaskListCreateGenericView,
                              TaskDetailGenericView,
                              get_stat
                               )
from my_app.views.subtask import (SubTaskListCreateGenericView,
                                SubTaskDetailGenericView
                               )
from my_app.views.category import CategoryViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet, 'categories')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),

    path('task/', TaskListCreateGenericView.as_view()),
    path('task/<int:pk>/', TaskDetailGenericView.as_view()),
    path('task/stat/', get_stat),

    path('subtasks/', SubTaskListCreateGenericView.as_view()),
    path('subtasks/<int:pk>/', SubTaskDetailGenericView.as_view()),
]

urlpatterns += router.urls
