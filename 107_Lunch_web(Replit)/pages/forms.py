from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput()
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput()
    )

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(
        label="新的密碼",
        widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label='確認密碼',
        widget=forms.PasswordInput()
    )