from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
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


@login_required
@request_student
def student(request, stud):
    user = MyUser.objects.filter(username=stud)
    base_book = BookWithClass.objects.filter(student_class__number_class=user[0].learned_class.number_class)
    contex = {
        'student': user[0],
        'books': base_book
    }
    return render(request, 'diary/student.html', contex)


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            if user.is_student:
                return redirect(f"student/{user.username}")
            return redirect('fdgdgfd/')
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
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                if user.is_student:
                    return redirect('student', stud=user.username)
                return redirect('teacher')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(request, 'diary/login.html', context={"login_form": form})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
@request_student
def homework(request, stud):
    model = MyUser.objects.filter(username=stud)
    h_work = HomeWorkModel.objects.filter(student_class=model[0].learned_class)
    context = {
        'user': model[0],
        'homework': h_work,
        'requests': request
    }
    return render(request, 'diary/homework.html', context=context)


@login_required
@request_teacher
def teacher(request):
    model = SchoolClass.objects.all()

    if request.method == 'POST':
        form = NewHomeWorkForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login/')

    form = NewHomeWorkForm()
    context = {
        'model': model,
        'form_homework': form,
    }
    return render(request, 'diary/teacher.html', context=context)


@login_required
@request_teacher
def learned_class(request, class_number, slug_name):
    model = MyUser.objects.filter(learned_class__slug=slug_name, learned_class__number_class=class_number)

    if request.method == 'POST':
        print(request.POST)
        form = SetEvaluationForm(request.POST)
        if form.is_valid():
            form.save()

    form = SetEvaluationForm()
    context = {
        'model': model,
        'form': form
    }
    return render(request, 'diary/learned_class.html', context=context)

# Create your views here.
