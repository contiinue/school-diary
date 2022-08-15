from django.urls import path
from diary.views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('student/<slug:stud>', student, name='student'),
    path('register/', RegisterUser, name='register'),
    path('login/', login, name='login')
]
