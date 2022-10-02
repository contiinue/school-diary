from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget

from diary.models import MyUser, HomeWorkModel, Evaluation
from django.contrib.admin.widgets import AdminDateWidget


class NewUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['learned_class'].empty_label = 'Не выбрано'
        self.fields['is_student'].empty_label = 'Не выбрано'

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Пдтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = MyUser
        fields = ('first_name', 'last_name',
                  "username", 'email', "password1", "password2",
                  'age', 'learned_class',
                  'is_student',
                  )

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'learned_class': forms.Select(attrs={'class': 'form-select'}),
            'is_student': forms.Select(attrs={'class': 'form-select'}),
        }

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewHomeWorkForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['item'].empty_label = 'Не выбрано'
        self.fields['student_class'].empty_label = 'Не выбрано'

    class Meta:
        model = HomeWorkModel
        fields = '__all__'

        widgets = {
            'item': forms.Select(attrs={'class': 'form-control'}),
            'student_class': forms.Select(attrs={'class': 'form-control'}),
            'home_work': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SetEvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['student', 'item', 'quarter', 'evaluation']

