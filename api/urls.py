from rest_framework import routers
from django.urls import path, include
from .views import ApiEvaluation, ApiSetEvaluation, SchoolTimetableApi

router = routers.DefaultRouter()
# router.register('timetable/(?P<class_number>\d+)/(?P<slug_name>\w+)', SchoolTimetableApi, basename='timetable')#
router.register('evaluation/(?P<class_number>\d+)/(?P<slug_name>\w+)', ApiEvaluation, basename='user-evaluation')
router.register('evaluation', ApiSetEvaluation, basename='evaluation')

urlpatterns = [
    path('', include(router.urls)),
    path(r'timetable/<int:class_number>/<slug:slug_name>/', SchoolTimetableApi.as_view(), name='timetable')
]
