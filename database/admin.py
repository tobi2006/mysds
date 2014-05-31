from django.contrib import admin
from database.models import MetaData, Course, Module, Student


class StudentAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name')
    search_fields = ('first_name', 'last_name')
    filter_horizontal = ('modules',)

admin.site.register(MetaData)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Student, StudentAdmin)
