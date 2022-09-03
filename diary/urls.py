from django.urls import path
from diary.views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('student/<slug:stud>', student, name='student'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('homework/<slug:stud>', homework, name='homework'),
    path('teacher', teacher, name='teacher'),
    path('student-class/<int:class_number>/<slug:slug_name>/', student_class, name='student-class')
]
