from .get_quarter import get_now_quarter, get_evaluation_of_quarter

from .models import *
from .utils import request_teacher, request_student
from .forms import MyUserForm, NewHomeWorkForm, SetEvaluationForm, StudentRegistrationForm, TeacherRegistrationForm

from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, FormView, TemplateView, View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404


class HomePage(TemplateView):
    """ Home-page  """
    template_name = 'diary/homepage.html'


class Register(View):
    """ Register form send to template  """
    template_name = 'diary/register.html'
    form = MyUserForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        """todo: Сделать проверку юзера первой т.к мродели не ученика
        todo: или учителя присваивается примери кей и невозможно сохранить юзера"""
        teacher_or_student_form = self.get_form()
        if teacher_or_student_form.is_valid():
            some = teacher_or_student_form.save(commit=True)
            print(some.pk, some)
            return self.form_valid(some)
        return render(request, self.template_name, teacher_or_student_form)

    def get_context_data(self, **kwargs):
        who_register = self.request.GET.get('register_teacher_or_student', False)
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
            return TeacherRegistrationForm(self.request.POST)

        if 'learned_class' in self.request.POST:
            return StudentRegistrationForm(self.request.POST)

    def form_valid(self, model_user):
        my_query = self.request.POST.copy()
        my_query['student'] = model_user.pk
        form_user = self.form(my_query)
        if form_user.is_valid():
            model_user.save()
            u = form_user.save()
            login(self.request, u)
            return redirect(reverse('student', kwargs={'username': u.username}))


class LoginUser(LoginView):
    """
    Login template return to console if user is teacher
    else return to profile user
    """
    template_name = 'diary/login.html'

    def get_success_url(self):
        if self.request.user.is_student == 'student':
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
            student_class=self.request.user.learned_class
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
            evaluations[book.book.book_name] = get_evaluation_of_quarter(
                self.request.user,
                book.book.book_name,
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


@login_required(login_url='login')
@request_student
def student(request, username):
    """ Student evaluation, get slug username and return student evaluations """
    user = get_object_or_404(MyUser, username=username)
    base_book = BookWithClass.objects.filter(student_class__number_class=user.learned_class.number_class)
    contex = {
        'student': user,
        'books': base_book
    }
    return render(request, 'diary/student.html', contex)


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


@login_required(login_url='login')
@request_teacher
def student_class(request, class_number, slug_name):
    """ Student class , get class and view students of this class """
    model = MyUser.objects.filter(learned_class__slug=slug_name, learned_class__number_class=class_number)

    if request.method == 'POST':
        form = SetEvaluationForm(request.POST)
        if form.is_valid():
            form.save()

    form = SetEvaluationForm()
    context = {
        'model': model,
        'form': form,
        'quarter': get_now_quarter().pk
    }
    return render(request, 'diary/student_class.html', context=context)
