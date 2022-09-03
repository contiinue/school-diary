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

# Register your models here.
