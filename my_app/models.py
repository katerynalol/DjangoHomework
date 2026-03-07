from datetime import datetime
from decimal import Decimal

from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator


STATUS_CHOICES = [
    ("New", "New task"),
    ("In progress", "Active task"),
    ("Pending", "Pending..."),
    ("Blocked", "Blocked"),
    ("Done", "Finished"),
    ]


class Task(models.Model):
    title: str = models.CharField(
        max_length=100,
        verbose_name="Название задачи",
        unique_for_date="created_at"
    )
    description: str = models.TextField(
        verbose_name="Описание задачи",
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(500)],
    )
    categories = models.ManyToManyField(
        'Category',
        related_name='tasks',
        verbose_name="Категория задачи")

    status: str = models.CharField(
        verbose_name="Статус задачи",
        max_length=20,
        choices=STATUS_CHOICES,
        default="New"
    )
    deadline: datetime = models.DateTimeField(
        verbose_name="Дата и время дедлайна"
    )
    created_at: datetime = models.DateTimeField(
        verbose_name="Дата и время создания",
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_task'
        verbose_name = "Task"
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['title'],
                name='unique_task'
            )
        ]


class SubTask(models.Model):
    title: str = models.CharField(
        max_length=100,
        verbose_name="Название подзадачи"
    )
    description: str = models.TextField(
        verbose_name="Описание подзадачи",
        validators=[
            MinLengthValidator(5),
            MaxLengthValidator(500)
        ]
    )
    task = models.ForeignKey(
        'Task',
        on_delete=models.PROTECT,
        related_name='subtasks'
    )
    status:str = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New"
    )
    deadline: datetime = models.DateTimeField(
        verbose_name="Дата и время дедлайна"
    )
    created_at: datetime = models.DateTimeField(
        verbose_name="Дата и время создания",
        auto_now_add=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        verbose_name = "SubTask"
        ordering = ['-created_at']

        constraints = [
            models.UniqueConstraint(
                fields=['title', 'task'],
                name='unique_subtask'
            )
        ]


class Category(models.Model):
    name: str = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название категории"
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = "Category"
        constraints = [
            models.UniqueConstraint(
                fields=['name'],
                name='unique_category'
            )
        ]