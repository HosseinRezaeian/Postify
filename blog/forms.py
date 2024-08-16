from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        label='user name',
        widget=forms.TextInput())

    password = forms.CharField(
        label="password",
        widget=forms.PasswordInput())
