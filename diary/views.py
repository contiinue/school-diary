from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic import ListView
from django.contrib import messages
from .forms import NewUserForm, NewHomeWorkForm, SetEvaluationForm
from .models import *
from .utils import request_teacher, request_student


class HomePage(ListView):
    model = MyUser
    template_name = 'diary/homepage.html'
    context_object_name = 'user'


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            if user.is_student == 'student':
                return redirect('student', stud=user.username)
            return redirect('teacher')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="diary/register.html", context={"register_form": form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, f"{username}.")
            if user.is_student == 'student':
                return redirect('student', stud=user.username, permanent=True)
            return redirect('teacher', permanent=True)
        messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(request, 'diary/login.html', context={"login_form": form})


def logout_user(request):
    logout(request)
    return redirect('home', permanent=True)


@login_required(login_url='login')
@request_student
def homework(request, stud):
    user = get_object_or_404(MyUser, username=stud)
    h_work = HomeWorkModel.objects.filter(student_class=user.learned_class)
    context = {
        'user': user,
        'homework': h_work,
        'requests': request
    }
    return render(request, 'diary/homework.html', context=context)


@login_required(login_url='login')
@request_student
def student(request, stud):
    user = get_object_or_404(MyUser, username=stud)
    base_book = BookWithClass.objects.filter(student_class__number_class=user.learned_class.number_class)

    contex = {
        'student': user,
        'books': base_book
    }
    return render(request, 'diary/student.html', contex)


@login_required(login_url='login')
@request_teacher
def teacher(request):
    model = SchoolClass.objects.all()

    if request.method == 'POST':
        form = NewHomeWorkForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            messages.error(request, "Форма заполненна не правильно")

    form = NewHomeWorkForm()
    context = {
        'model': model,
        'form_homework': form,
    }
    return render(request, 'diary/teacher.html', context=context)


@login_required(login_url='login')
@request_teacher
def student_class(request, class_number, slug_name):
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

# Create your views here.
