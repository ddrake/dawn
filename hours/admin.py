from django.contrib import admin

from hours.models import Language, Task, TaskTranslation, Profile


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

class ProfileAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['username', 'first_name', 'last_name', 'email',
                    'is_staff', 'user_instructions_email', 'help_emailed'] 

admin.site.register(Language, LanguageAdmin)
admin.site.register(Task, TaskAdmin)
admin.site.register(Profile, ProfileAdmin)
