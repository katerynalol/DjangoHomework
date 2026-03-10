from datetime import timedelta
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q, F
from my_app.models import *


new_task = Task.objects.create(
    title="Prepare presentation",
    description="Prepare materials and slides for the presentation",
    deadline=timezone.now() + timedelta(days=3)
)
print("create")
print(new_task)

parent_task = Task.objects.get(title="Prepare presentation")

new_subtask = SubTask.objects.create(
    task=parent_task,
    title="Gather information",
    description="Find necessary information for the presentation",
    deadline=timezone.now() + timedelta(days=2)
)
print("create")
print(new_subtask)



new_another_subtask = SubTask.objects.create(
    task=parent_task,
    title="Create slides",
    description="Create presentation slides",
    deadline=timezone.now() + timedelta(days=1)
)
print("create")
print(new_another_subtask)

# ---------------------------------------------------------------------------------------------------------------------

task_new_status = Task.objects.filter(
    status="New"
)
for obj in task_new_status:
    print(obj.title, obj.status)

print("------" * 50)

now_date = datetime.today()
subtask = SubTask.objects.filter(
    Q(status="Done") & Q(deadline__lte=now_date)
)
for obj in subtask:
    print(obj.title, obj.status, obj.deadline)

# ---------------------------------------------------------------------------------------------------------------------

update_status_task = Task.objects.filter(
    title="Prepare presentation"
).update(status="In progress")

task_update_status = Task.objects.get(title="Prepare presentation")
print(task_update_status.title, task_update_status.status)


update_deadline_subtask = SubTask.objects.filter(
    title="Gather information"
).update(deadline=timezone.now() - timedelta(days=2))

subtask_update_deadline = SubTask.objects.get(title="Gather information")
print(subtask_update_deadline.title, subtask_update_deadline.deadline)


update_description_subtask = SubTask.objects.filter(
    title="Create slides"
).update(description="Create and format presentation slides")

subtask_update_description = SubTask.objects.get(title="Create slides")
print(subtask_update_description.title, subtask_update_description.description)

# --------------------------------------------------------------------------------------------------------------------

task_delete = Task.objects.get(
    title="Prepare presentation"
)
task_delete.delete()

all_tasks = Task.objects.all()
for task in all_tasks:
    print(task.title)

all_subtasks = SubTask.objects.all()
for subtask in all_subtasks:
    print(subtask.title)