from django import forms
from django.contrib.auth.forms import UserCreationForm
from diary.models import MyUser, HomeWorkModel, Evaluation


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ("username", "email", "password1", "password2", 'age', 'learned_class', 'is_student')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NewHomeWorkForm(forms.ModelForm):
    class Meta:
        model = HomeWorkModel
        fields = '__all__'


class SetEvaluationForm(forms.ModelForm):

    class Meta:
        model = Evaluation
        fields = ['student', 'item', 'evaluation']