from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=16)
    password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput)


class SignupForm(forms.Form):
    username = forms.CharField(label="Username", max_length=16)
    email = forms.EmailField(label="E-mail", max_length=32, widget=forms.EmailInput)
    password = forms.CharField(label="Password", max_length=32, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm password", max_length=32, widget=forms.PasswordInput)


class SettingsForm(forms.Form):
    description = forms.CharField(label="Description", max_length=300, widget=forms.Textarea, required=False)
    avatar = forms.ImageField(required=False)
