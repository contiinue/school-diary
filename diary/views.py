from django.http import HttpResponse
from django.views.generic.base import TemplateResponseMixin

from services.excel_evaluations import get_excel
from services.get_evaluations_of_quarter import get_now_quarter, get_evaluation_of_quarter

from .models import *
from .utils import request_student, request_teacher
from .forms import MyUserForm, NewHomeWorkForm, StudentRegistrationForm, TeacherRegistrationForm

from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, FormView, TemplateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


class HomePage(TemplateView):
    """ Home-page  """
    template_name = 'diary/homepage.html'


class Register(View, TemplateResponseMixin):
    """ 
    :todo посмотреть-сделать миксины и уменьшить килечество кода
    :todo убрать дублирование render_to_response
    Register form send to template  
    """
    template_name = 'diary/register.html'
    form = MyUserForm
    success_url = 'student'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        user_form = self.form(request.POST)
        if user_form.is_valid():
            return self.form_valid(
                user_form.save(commit=False)
            )
        return self.render_to_response({'user': user_form, 'registration': self.get_form()})

    def get_context_data(self, **kwargs):
        who_register = self.request.GET.get('register_teacher_or_student')
        kwargs['user'] = MyUserForm
        if who_register == 'teacher':
            kwargs['registration'] = TeacherRegistrationForm
        elif who_register == 'student':
            kwargs['registration'] = StudentRegistrationForm
        else:
            return {}
        return kwargs

    def get_form(self) -> TeacherRegistrationForm | StudentRegistrationForm:
        if 'item' in self.request.POST:
            self.success_url = 'teacher'
            return TeacherRegistrationForm(self.request.POST)

        if 'learned_class' in self.request.POST:
            return StudentRegistrationForm(self.request.POST)

    def form_valid(self, user_model):
        form_teacher_or_student = self.get_form()
        if form_teacher_or_student.is_valid():
            stud_or_teach_model = form_teacher_or_student.save()
            user = self.save_user(user_model, stud_or_teach_model)
            login(self.request, user)
            return redirect(self.get_success_url())
        return self.render_to_response(
            {'user': self.form(self.request.POST), 'registration': self.get_form()}
        )

    @staticmethod
    def save_user(user_model: MyUser, student_or_teacher_model: StudentRegistration | TeacherRegistration) -> MyUser:
        if isinstance(student_or_teacher_model, TeacherRegistration):
            user_model.teacher = student_or_teacher_model
            user_model.save()
            return user_model
        user_model.student = student_or_teacher_model
        user_model.save()
        return user_model

    def get_success_url(self):
        if self.success_url == 'student':
            return reverse_lazy('student', kwargs={'username': self.request.user.username})
        return reverse_lazy('teacher')


class LoginUser(LoginView):
    """
    Login template return to console if user is teacher
    else return to profile user
    """
    template_name = 'diary/login.html'

    def get_success_url(self):
        if isinstance(self.request.user.student, StudentRegistration):
            return reverse_lazy('student', kwargs={'username': self.request.user.username})
        return reverse_lazy('teacher')


def logout_user(request):
    logout(request)
    return redirect('home', permanent=True)


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(request_student, name='dispatch')
class HomeWork(ListView):
    """ Student homework """
    template_name = 'diary/homework.html'
    model = HomeWorkModel
    context_object_name = 'homework'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(
            student_class=self.request.user.student.learned_class.number_class
        )

    def get_context_data(self, **kwargs):
        context = super(HomeWork, self).get_context_data(**kwargs)
        context['requests'] = self.request
        return context


class Student(ListView):
    model = BookWithClass
    template_name = 'diary/student.html'
    context_object_name = 'books'

    def get_queryset(self):
        qs = super().get_queryset()
        evaluations = dict()
        for book in qs:
            evaluations[book.time_table.item.book_name] = get_evaluation_of_quarter(
                self.request.user,
                book.time_table.item.book_name,
                self.request.GET.get('quarter')
            )
        return evaluations

    def get_context_data(self, **kwargs):
        context = super(Student, self).get_context_data(**kwargs)
        context['now_quarter'] = get_now_quarter()
        context['all_quarter'] = Quarter.objects.all()
        request_quarter = self.request.GET.get('quarter', None)
        context['request_quarter'] = int(request_quarter) if request_quarter else get_now_quarter().pk

        return context


class Teacher(FormView):
    """ Teacher console, teacher can set homework and move to class   """
    template_name = 'diary/teacher.html'
    form_class = NewHomeWorkForm
    success_url = 'teacher'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = SchoolClass.objects.all()
        return context


class StudentsClass(ListView):
    """ todo: user.evaluation_set.filter(quarter=some_quarter) """
    template_name = 'diary/student_class.html'
    queryset = Quarter.objects.all()
    context_object_name = 'quarters'


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(request_teacher, name='dispatch')
def download_evaluations(request, class_number, slug_name):
    file_data = get_excel(
        request.user.teacher.item.book_name, class_number, slug_name
    )
    response = HttpResponse(file_data, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="foo.xls"'
    return response
