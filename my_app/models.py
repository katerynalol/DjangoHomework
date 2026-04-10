from datetime import datetime

from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils import timezone


STATUS_CHOICES = [
    ("New", "New task"),
    ("In progress", "Active task"),
    ("Pending", "Pending..."),
    ("Blocked", "Blocked"),
    ("Done", "Finished"),
    ]


class CategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

    def get_all_with_deleted(self):
        return super().get_queryset()


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
        on_delete=models.CASCADE,
        related_name='subtasks',
        verbose_name='Основная задача'
    )
    status:str = models.CharField(
        verbose_name="Статус подзадачи",
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

# Задание 2: Реализация мягкого удаления категорий
# Шаги для выполнения:
# Добавьте два новых поля в вашу модель Category, если таких ещё не было.
# В модели Category добавьте поля is_deleted(Boolean, default False) и deleted_at(DateTime, null=true)
# Переопределите метод удаления, чтобы он обновлял новые поля к соответствующим значениям: is_deleted=True и дата и время на момент “удаления” записи
# Переопределите менеджера модели Category
# В менеджере модели переопределите метод get_queryset(), чтобы он по умолчанию выдавал только те записи, которые не “удалены” из базы.
class Category(models.Model):
    name: str = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Название категории"
    )
    is_deleted = models.BooleanField(
        default=False
    )
    deleted_at: datetime = models.DateTimeField(
        verbose_name="Дата и время удаления",
        null=True,
        blank=True
    )

    objects = CategoryManager()
    all_objects = models.Manager()

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

    def delete(self, using = None, keep_parents = False):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()