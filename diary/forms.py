from django import forms
from django.contrib.auth.forms import UserCreationForm
from diary.models import MyUser


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
