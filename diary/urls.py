from django.urls import path
from diary.views import (
    HomePage,
    Student,
    Teacher,
    Register,
    LoginUser,
    logout_user,
    HomeWork,
    StudentsClass,
    download_evaluations,
    SchoolPayment,
    SuccessPyment,
    CanselPyment,
)

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("student/<slug:username>", Student.as_view(), name="student"),
    path("teacher", Teacher.as_view(), name="teacher"),
    path("register/", Register.as_view(), name="register"),
    path("login/", LoginUser.as_view(), name="login"),
    path("logout", logout_user, name="logout"),
    path("homework/<slug:username>", HomeWork.as_view(), name="homework"),
    path(
        "student-class/<int:class_number>/<slug:slug_name>/",
        StudentsClass.as_view(),
        name="student-class",
    ),
    path(
        "student-class/<int:class_number>/<slug:slug_name>/download/",
        download_evaluations,
        name="download-evaluations",
    ),
    path("payment/", SchoolPayment.as_view(), name="school-payment"),
    path("success-payment/", SuccessPyment.as_view(), name="success-payment"),
    path("cansel-payment/", CanselPyment.as_view(), name="cansel-payment"),
]
