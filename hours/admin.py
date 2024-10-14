from django.contrib import admin

from hours.models import Language, Task, TaskTranslation


class TaskTranslationInline(admin.TabularInline):
    model = TaskTranslation
    fk_name = "task"

    def get_max_num(self, request, obj=None, **kwargs):
        return 2


class TaskAdmin(admin.ModelAdmin):
    inlines = [
        TaskTranslationInline,
    ]


class LanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Language, LanguageAdmin)
admin.site.register(Task, TaskAdmin)
