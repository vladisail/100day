import re
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password2']

    def clean_username(self):
        username = self.cleaned_data['username']
        # Проверяем, существует ли пользователь с таким логином
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким логином уже существует.')
        return username

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают.')
        return password2

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(
                r'[0-9]', password):
            raise forms.ValidationError(
                'Пароль должен содержать минимум 8 символов, включая латинские буквы в верхнем и нижнем регистре, и цифры.')
        return password


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth', 'photo']

    widgets = {
        'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
        'photo': forms.FileInput(attrs={'class': 'file-input'}),
    }


class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label='Old Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
    )
    new_password1 = forms.CharField(
        label='New Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )
    new_password2 = forms.CharField(
        label='Confirm New Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')



class AddFriendForm(forms.Form):
    friend_username = forms.CharField(label='Username')

class SearchFriendsForm(forms.Form):
    search_query = forms.CharField(label='Search')
