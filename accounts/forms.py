from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Enter your username...", max_length=16)
    password = forms.CharField(label="Enter your password...", max_length=32, widget=forms.PasswordInput)
