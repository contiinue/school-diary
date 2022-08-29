from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import ListView
from django.contrib import messages
from .forms import NewUserForm, NewHomeWorkForm, SetEvaluationForm
from .models import *


class HomePage(ListView):
    model = MyUser
    template_name = 'diary/homepage.html'
    context_object_name = 'user'


def student(request, stud):
    model = MyUser.objects.filter(username=stud)
    contex = {
        'student': model[0]
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


def loginuser(request):
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
                    return redirect(f'student', stud=user.username)
                return redirect('teacher')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()

    return render(request, 'diary/login.html', context={"login_form": form})


def homework(request, stud):
    model = MyUser.objects.filter(username=stud)
    h_work = HomeWorkModel.objects.filter(student_class=model[0].learned_class)
    context = {
        'user': model[0],
        'homework': h_work,
        'requests': request
    }
    # проверка на аундифекацию юзера
    # if request.user.username != model[0].username:
    #     return redirect('login')

    return render(request, 'diary/homework.html', context=context)


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


def learned_class(request, cla):
    model = MyUser.objects.filter(learned_class=cla)

    if request.method == 'POST':
        print(request.POST)
        form = SetEvaluationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    form = SetEvaluationForm()
    context = {
        'model': model,
        'form': form
    }
    return render(request, 'diary/learned_class.html', context=context)

# Create your views here.
