from django.urls import path
from diary.views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),

    path('student/<slug:username>', Student.as_view(), name='student'),
    path('teacher', Teacher.as_view(), name='teacher'),

    path('register/', Register.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout', logout_user, name='logout'),

    path('homework/<slug:username>', HomeWork.as_view(), name='homework'),
    path('student-class/<int:class_number>/<slug:slug_name>/', student_class, name='student-class'),
]

