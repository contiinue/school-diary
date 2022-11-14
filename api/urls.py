from rest_framework import routers
from django.urls import path, include
from .views import ApiSetEvaluation, SchoolTimetableApi, MyUserApi, StudentApi

router = routers.DefaultRouter()
router.register('evaluation', ApiSetEvaluation, basename='evaluation')
router.register('user', MyUserApi)
router.register('student', StudentApi)


urlpatterns = [
    path('', include(router.urls)),
    path(r'timetable/<int:class_number>/<slug:slug_name>/', SchoolTimetableApi.as_view(), name='timetable'),
]
