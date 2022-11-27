from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.base import TemplateResponseMixin

from services.excel_evaluations import get_excel
from services.get_evaluations_of_quarter import (
    get_now_quarter,
    get_evaluation_of_quarter,
)

from schooldiary.settings import invitation_token_expiration_date
from .models import *
from .utils import request_student, request_teacher
from .forms import (
    MyUserForm,
    NewHomeWorkForm,
    StudentRegistrationForm,
    TeacherRegistrationForm,
)

from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, FormView, TemplateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime


class HomePage(TemplateView):
    """Home-page"""

    template_name = "diary/homepage.html"


class Register(View, TemplateResponseMixin):
    template_name = "diary/register.html"
    form = MyUserForm
    success_url = "student"

    def get(self, request):
        """
        Get Forms(student and teacher or student) for registration if request is true
        else get default page
        """
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
        """Register student or teacher if forms is valid then Redirect else return form once again"""
        form_student_or_teacher = self.get_form_for_teacher_or_student()(request.POST)
        form = self.form(request.POST)
        token = self.get_token(form)
        if form_student_or_teacher.is_valid() and form.is_valid():
            return self.form_valid(form, form_student_or_teacher, token)
        else:
            return self.form_invalid(form, form_student_or_teacher)

    def form_invalid(
        self,
        form: MyUserForm,
        form_student_or_teacher: StudentRegistrationForm | TeacherRegistrationForm,
    ):
        """Return invalid form"""
        return self.render_to_response(
            {"user": form, "registration": form_student_or_teacher}
        )

    def get_token(self, form: MyUserForm):
        """Return token if his is valid and did add < 2 days age"""
        try:
            token = TokenRegistration.objects.get(
                token=self.request.POST.get("invitation_token")
            )
            if (
                datetime.today().date() - token.date_token_create
                > invitation_token_expiration_date
            ):
                return form.add_error("invitation_token", "Срок действия токена истек")

            elif not token.who_registration == self.request.GET.get("request_form"):
                return form.add_error("invitation_token", "Не корректный токен")

            else:
                return token
        except ObjectDoesNotExist:
            return form.add_error("invitation_token", "Не корректный токен")

    def form_valid(
        self,
        form: MyUserForm,
        form_student_or_teacher: StudentRegistrationForm | TeacherRegistrationForm,
        token: TokenRegistration,
    ):
        """
        Save user to model.
        If registration form of student, save student else save teacher
        """
        model_user = form.save(commit=False)
        model_user.school = token.school
        teacher_or_student = form_student_or_teacher.save(commit=False)
        if isinstance(form_student_or_teacher, StudentRegistrationForm):
            teacher_or_student.learned_class = token.student_class
            model_user.student = teacher_or_student
            self.save_user(model_user, teacher_or_student)
        else:
            model_user.teacher = teacher_or_student
            self.save_user(model_user, teacher_or_student)
            self.success_url = "teacher"
        token.delete()
        return self.get_success_url(model_user)

    def save_user(self, model_user, teacher_or_student) -> None:
        """Save User to model and login his"""
        teacher_or_student.save()
        model_user.save()
        login(self.request, model_user)

    def get_form_for_teacher_or_student(self):
        """Return form of get request else return none."""
        if self.request.GET.get("request_form") == "student":
            return StudentRegistrationForm
        elif self.request.GET.get("request_form") == "teacher":
            return TeacherRegistrationForm

    def get_context_data(self, **kwargs) -> dict:
        """Return User registration form and form for teacher or student."""
        kwargs["user"] = self.form
        kwargs["registration"] = self.get_form_for_teacher_or_student()
        return kwargs

    def get_success_url(self, user) -> HttpResponseRedirect:
        """Redirect to student profile or teacher console after registration."""
        if self.success_url == "student":
            return HttpResponseRedirect(
                reverse_lazy("student", kwargs={"username": user.username})
            )
        return HttpResponseRedirect(reverse_lazy("teacher"))


class LoginUser(LoginView):
    """
    Login template return to console if user is teacher
    else return to profile user
    """

    template_name = "diary/login.html"

    def get_success_url(self):
        if isinstance(self.request.user.student, StudentRegistration):
            return reverse_lazy(
                "student", kwargs={"username": self.request.user.username}
            )
        return reverse_lazy("teacher")


def logout_user(request):
    logout(request)
    return redirect("home", permanent=True)


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(request_student, name="dispatch")
class HomeWork(ListView):
    """Student homework"""

    template_name = "diary/homework.html"
    model = HomeWorkModel
    context_object_name = "homework"

    def get_queryset(self):
        self.queryset = HomeWorkModel.objects.filter(
            student_class=self.request.user.student.learned_class.number_class
        )
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super(HomeWork, self).get_context_data(**kwargs)
        context["requests"] = self.request
        return context


class Student(ListView):
    model = BookWithClass
    template_name = "diary/student.html"
    context_object_name = "books"

    def get_queryset(self):
        qs = super().get_queryset()
        evaluations = dict()
        for book in qs:
            evaluations[book.time_table.item.book_name] = get_evaluation_of_quarter(
                self.request.user,
                book.time_table.item.book_name,
                self.request.GET.get("quarter"),
            )
        return evaluations

    def get_context_data(self, **kwargs):
        context = super(Student, self).get_context_data(**kwargs)
        context["now_quarter"] = get_now_quarter()
        context["all_quarter"] = Quarter.objects.all()
        request_quarter = self.request.GET.get("quarter", None)
        context["request_quarter"] = (
            int(request_quarter) if request_quarter else get_now_quarter().pk
        )

        return context


class Teacher(FormView):
    """Teacher console, teacher can set homework and move to class."""

    template_name = "diary/teacher.html"
    form_class = NewHomeWorkForm
    success_url = "teacher"

    def form_valid(self, form):
        """save Homework model."""
        model_homework = form.save(commit=False)
        model_homework.school = self.request.user.school
        model_homework.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """Get all student class of school."""
        context = super().get_context_data(**kwargs)
        context["model"] = SchoolClass.objects.filter(school=self.request.user.school)
        return context


class StudentsClass(ListView):
    template_name = "diary/student_class.html"
    queryset = Quarter.objects.all()
    context_object_name = "quarters"


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(request_teacher, name="dispatch")
def download_evaluations(request, class_number, slug_name):
    file_data = get_excel(request.user.teacher.item.book_name, class_number, slug_name)
    response = HttpResponse(file_data, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="foo.xls"'
    return response
