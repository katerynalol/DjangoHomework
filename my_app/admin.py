from django.contrib import admin
from my_app.models import *


class SubTaskInline(admin.StackedInline):
    model = SubTask


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "short_title",
        "status",
        "deadline"
    ]
    search_fields = ["title"]
    list_filter = [
        "status",
        "categories",
    ]
    list_editable = [
        "status"
    ]
    list_per_page = 10
    inlines = [
        SubTaskInline
    ]
    def short_title(self, obj):
        if len(obj.title) > 10:
            return obj.title[:10]+'...'
        return obj.title

    short_title.short_description = "Название"
    short_title.admin_order_field = "title"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "task",
        "status",
        "deadline"
    ]
    search_fields = ["title"]
    list_filter = [
        "status",
        "task",
    ]
    list_editable = [
        "status"
    ]
    list_per_page = 10

    actions = ["mark_as_done"]
    def mark_as_done(self, request, queryset):
        queryset.update(status="Done")
        self.message_user(request, "Выбранные подзадачи переведены в статус Done")
    mark_as_done.short_description = "Перевести выбранные подзадачи в Done"



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name"
    ]
    search_fields = ["name"]
    list_per_page = 10


# admin.site.register(Task)
# admin.site.register(SubTask)
# admin.site.register(Category)