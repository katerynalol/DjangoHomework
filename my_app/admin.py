from django.contrib import admin
from my_app.models import *


admin.site.register(Task)
admin.site.register(SubTask)
admin.site.register(Category)