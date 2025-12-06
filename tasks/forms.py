
from tasks.admin import TaskAdminForm


class TaskCreateForm(TaskAdminForm):
    class Meta(TaskAdminForm.Meta):
        fields = (
            'title',
            'description',
            'priority',
            'executor',
            'deadline',
        )
