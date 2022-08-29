from django.urls import path
from diary.views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('student/<slug:stud>', student, name='student'),
    path('register/', register, name='register'),
    path('login/', loginuser, name='login'),
    path('homework/<slug:stud>', homework, name='homework'),
    path('teacher', teacher, name='teacher'),
    path('student-class/<slug:cla>', learned_class, name='student-class')
]
