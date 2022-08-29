from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *


admin.site.register(MyUser, UserAdmin)
admin.site.register(Books)
admin.site.register(Evaluation)
admin.site.register(HomeWorkModel)
admin.site.register(SchoolClass)
# Register your models here.
