from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import CalendarUser

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label = 'Password', widget=forms.PasswordInput)

    class Meta:
        model = CalendarUser
        fields = ('email', 'username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CalendarUser
        fields = ('email', 'username',)

    def clean_password(self):
        return self.initial['password']