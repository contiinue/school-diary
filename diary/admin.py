from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import (
    MyUser,
    HomeWorkModel,
    SchoolSubjects,
    Evaluation,
    SchoolClass,
    BookWithClass,
    Quarter,
    SchoolTimetable,
    DayOfWeak,
    TokenRegistration,
    School,
)


class SchoolClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name_class",)}


admin.site.register(MyUser, UserAdmin)
admin.site.register(HomeWorkModel)
admin.site.register(SchoolSubjects)
admin.site.register(Evaluation)
admin.site.register(SchoolClass, SchoolClassAdmin)
admin.site.register(BookWithClass)
admin.site.register(Quarter)
admin.site.register(SchoolTimetable)
admin.site.register(DayOfWeak)
admin.site.register(TokenRegistration)
admin.site.register(School)

# Register your models here.
