from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView, TemplateView, View
from django.views.generic.base import TemplateResponseMixin

from schooldiary.settings import invitation_token_expiration_date
from services.excel_evaluations import get_excel
from services.get_evaluations_of_quarter import (
    get_evaluation_of_quarter,
    get_now_quarter,
)

from .forms import (
    MyUserForm,
    NewHomeWorkForm,
    StudentRegistrationForm,
    TeacherRegistrationForm,
)
from .models import (
    BookWithClass,
    HomeWorkModel,
    Quarter,
    SchoolClass,
    StudentRegistration,
    TokenRegistration,
)
from .utils import request_student, request_teacher


class HomePage(TemplateView):
    """Home-page"""

    template_name = "diary/homepage.html"


class Register(View, TemplateResponseMixin):
    template_name = "diary/register.html"
    form = MyUserForm
    success_url = "student"

    def get(self, request):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request):
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
        return self.render_to_response(
            {"user": form, "registration": form_student_or_teacher}
        )

    def get_token(self, form: MyUserForm):
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
        model_user = form.save(commit=False)
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
        teacher_or_student.save()
        model_user.save()
        login(self.request, model_user)

    def get_form_for_teacher_or_student(self):
        if self.request.GET.get("request_form") == "student":
            return StudentRegistrationForm
        elif self.request.GET.get("request_form") == "teacher":
            return TeacherRegistrationForm

    def get_context_data(self, **kwargs) -> dict:
        kwargs["user"] = self.form
        kwargs["registration"] = self.get_form_for_teacher_or_student()
        return kwargs

    def get_success_url(self, user) -> reverse_lazy:
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
        qs = super().get_queryset()
        return qs.filter(
            student_class=self.request.user.student.learned_class.number_class
        )

    def get_context_data(self, **kwargs):
        context = super(HomeWork, self).get_context_data(**kwargs)
        context["requests"] = self.request
        return context


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(request_student, name="dispatch")
class Student(ListView):
    model = BookWithClass
    template_name = "diary/student.html"
    context_object_name = "books"

    def get_queryset(self, **kwargs):
        qs = super().get_queryset()
        for book in qs:
            kwargs[book.time_table.item.book_name] = get_evaluation_of_quarter(
                self.request.user,
                book.time_table.item.book_name,
                self.request.GET.get("quarter"),
            )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(Student, self).get_context_data(**kwargs)
        context["now_quarter"] = get_now_quarter()
        context["all_quarter"] = Quarter.objects.all()
        request_quarter = self.request.GET.get("quarter", None)
        context["request_quarter"] = (
            int(request_quarter) if request_quarter else get_now_quarter().pk
        )

        return context


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(request_teacher, name="dispatch")
class Teacher(FormView):
    """Teacher console, teacher can set homework and move to class."""

    template_name = "diary/teacher.html"
    form_class = NewHomeWorkForm
    success_url = "teacher"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model"] = SchoolClass.objects.all()
        return context


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(request_teacher, name="dispatch")
class StudentsClass(ListView):
    template_name = "diary/student_class.html"
    queryset = Quarter.objects.all().order_by("start")
    context_object_name = "quarters"


@method_decorator(login_required(login_url="login"), name="dispatch")
@method_decorator(request_teacher, name="dispatch")
def download_evaluations(request, class_number, slug_name):
    file_data = get_excel(request.user.teacher.item.book_name, class_number, slug_name)
    response = HttpResponse(file_data, content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = 'attachment; filename="foo.xls"'
    return response
