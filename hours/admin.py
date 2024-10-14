from django.contrib import admin

from hours.models import Task, TaskTranslation


class TaskTranslationInline(admin.TabularInline):
    model = TaskTranslation
    fk_name = "task"

    def get_max_num(self, request, obj=None, **kwargs):
        return 2


class TaskAdmin(admin.ModelAdmin):
    inlines = [
        TaskTranslationInline,
    ]


admin.site.register(Task, TaskAdmin)
