from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'id': 'login-email',
            'placeholder': 'آدرس ایمیل'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'id': 'login-pass',
            'placeholder': 'کلمه عبور'

        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'id': 'login-pass',
            'placeholder': 'تکرار کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('کلمه عبور و تکرار کلمه عبور با یکدیگر مغایرت دارند')


class ForgotPassword(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'id': 'login-email',
            'placeholder': 'ایمیل'
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'id': 'login-email',
            'placeholder': 'آدرس ایمیل'
        }),
        error_messages={
            'required': "لطفا ایمیل خود را وارد کنید"
        },
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'id': 'login-pass',
            'placeholder': 'کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )


class ActivateAccount(forms.Form):
    email_active_code = forms.CharField(
        label='کد فعالسازی',
        widget=forms.TextInput(attrs={
            'id': 'login-email',
            'placeholder': 'کد فعالسازی'
        }),
        validators=[
            validators.MaxLengthValidator(6)
        ]
    )


class ResetPassword(forms.Form):
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'login-pass',
            'placeholder': 'کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'login-pass',
            'placeholder': 'تکرار کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        ValidationError('کلمه عبور و تکرار کلمه عبور با یکدیگر مغایرت دارند')
