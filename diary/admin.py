from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


class SchoolClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name_class',)}


admin.site.register(MyUser, UserAdmin)
admin.site.register(HomeWorkModel)
admin.site.register(Books)
admin.site.register(Evaluation)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(BookWithClass)
admin.site.register(Quarter)
admin.site.register(SchoolTimetable)
admin.site.register(DayOfWeak)
admin.site.register(TokenRegistration)

# Register your models here.
