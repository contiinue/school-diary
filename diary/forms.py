from django import forms
from django.contrib.auth.forms import UserCreationForm

from diary.models import (
    Evaluation,
    HomeWorkModel,
    MyUser,
    StudentRegistration,
    TeacherRegistration,
)


class MyUserForm(UserCreationForm):
    """Register User."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    username = forms.CharField(
        label="Логин", widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = MyUser
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
            "invitation_token",
        )

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control for_test"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "invitation_token": forms.TextInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

    def save(self, commit=True):
        user = super(MyUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class TeacherRegistrationForm(forms.ModelForm):
    class Meta:
        model = TeacherRegistration
        fields = ["age", "item"]

        widgets = {
            "age": forms.TextInput(attrs={"class": "form-control"}),
            "item": forms.Select(attrs={"class": "form-control"}),
        }


class StudentRegistrationForm(forms.ModelForm):
    """ """

    class Meta:
        model = StudentRegistration
        fields = ("age",)

        widgets = {
            "age": forms.TextInput(attrs={"class": "form-control"}),
        }


class NewHomeWorkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["item"].empty_label = "Не выбрано"
        self.fields["student_class"].empty_label = "Не выбрано"

    class Meta:
        model = HomeWorkModel
        fields = ("item", "student_class", "home_work", "date_end_of_homework")

        widgets = {
            "item": forms.Select(attrs={"class": "form-control"}),
            "student_class": forms.Select(attrs={"class": "form-control"}),
            "home_work": forms.TextInput(attrs={"class": "form-control"}),
            "date_end_of_homework": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
        }


class SetEvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ["student", "item", "quarter", "evaluation"]


class PaymentForm(forms.Form):
    count_month = forms.IntegerField(max_value=24)
