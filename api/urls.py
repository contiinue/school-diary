from django.urls import include, path
from rest_framework import routers

from .views import ApiSetEvaluation, MyUserApi, SchoolTimetableApi, StudentApi

router = routers.DefaultRouter()
router.register("evaluation", ApiSetEvaluation, basename="evaluation")
router.register("user", MyUserApi)
router.register("student", StudentApi)


urlpatterns = [
    path("", include(router.urls)),
    path(
        r"timetable/<int:class_number>/<slug:slug_name>/",
        SchoolTimetableApi.as_view(),
        name="timetable",
    ),
]
