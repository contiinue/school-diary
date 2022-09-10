from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.views.generic import ListView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .utils import request_teacher, request_student
from .forms import NewUserForm, NewHomeWorkForm, SetEvaluationForm


class HomePage(ListView):
    """ Home-page  """
    model = MyUser
    template_name = 'diary/homepage.html'
    context_object_name = 'user'


class Register(FormView):
    """ Register form send to template  """
    template_name = 'diary/register.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        if user.is_student == 'teacher':
            return redirect('teacher')
        return redirect(reverse('student', kwargs={'username': user.username}))


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
            student_class=self.request.user.learned_class)

    def get_context_data(self, **kwargs):
        context = super(HomeWork, self).get_context_data(**kwargs)
        context['requests'] = self.request
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
        'form': form
    }
    return render(request, 'diary/student_class.html', context=context)
