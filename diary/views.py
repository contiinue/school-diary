from .get_quarter import get_now_quarter, get_evaluation_of_quarter

from .models import *
from .utils import request_teacher, request_student, get_teacher_or_student_form, save_user_to_model
from .forms import MyUserForm, NewHomeWorkForm, SetEvaluationForm, StudentRegistrationForm, TeacherRegistrationForm

from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
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
    form_class = MyUserForm

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        q = request.POST.copy()
        register, who_register = get_teacher_or_student_form(request.POST)
        user_form = save_user_to_model(request, register)
        if isinstance(register, (StudentRegistrationForm, TeacherRegistrationForm)):
            return render(request, self.template_name, context={'user': user_form, 'registration': register})
        if isinstance(user_form, MyUserForm):
            return render(request, self.template_name, context={'user': user_form, 'registration': register})
        login(request, user_form)
        if who_register == 'student':
            return redirect(reverse('student', kwargs={'username': user_form.username}))
        return redirect('teacher')

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

    # def form_valid(self, form):
    #     user = form.save()
    #     login(self.request, user)
    #     if user.is_student == 'teacher':
    #         return redirect('teacher')
    #     return redirect(reverse('student', kwargs={'username': user.username}))


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
