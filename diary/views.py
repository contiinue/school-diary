from django.shortcuts import render
from django.views.generic import ListView

from diary.models import Students


#def index(request):
#    return render(request, 'diary/show_student.html')


class HomePage(ListView):
    model = Students
    template_name = 'diary/show_student.html'
    context_object_name = 'user'


def student(request, stud):
    contex = {
        'student': stud
    }
    return render(request, 'diary/student.html', contex)


def RegisterUser():
    pass


def login():
    pass

# Create your views here.
