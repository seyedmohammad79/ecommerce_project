from django.contrib.auth import login, logout
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

from account_module.forms import LoginForm, RegisterForm, ActivateAccount, ForgotPassword, ResetPassword
from account_module.models import User

import random

from utils.email_service import send_email


# Create your views here.


class SignUp(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/sign-up.html', context)

    def post(self, request: HttpRequest):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده قبلا ثبت نام شده است')
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=str(random.randrange(100000, 999999)),
                    email_active_url=get_random_string(72),
                    is_active=False,
                    username=user_email)
                new_user.set_password(user_password)
                new_user.save()
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user}, 'email.html')
                return redirect(reverse('activate_account', args=[new_user.email_active_url]))
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/sign-up.html', context)


class ActivateUserView(View):
    def get(self, request: HttpRequest, email_active_url):
        user: User = User.objects.filter(email_active_url__iexact=email_active_url).first()
        if user is not None:
            if not user.is_active:
                activate_form = ActivateAccount()
                context = {
                    'activate_form': activate_form,
                    'email_active_url': email_active_url
                }
                return render(request, 'account_module/email_authenticate.html', context)
            else:
                return redirect(reverse('login-page'))
        raise Http404

    def post(self, request: HttpRequest, email_active_url):
        activate_form = ActivateAccount(request.POST)
        if activate_form.is_valid():
            user: User = User.objects.filter(email_active_url__iexact=email_active_url, is_active=False).first()
            if user is not None:
                user_code = activate_form.cleaned_data.get('email_active_code')
                if str(user.email_active_code) == user_code:
                    user.is_active = True
                    user.email_active_code = str(random.randrange(100000, 999999))
                    user.email_active_url = get_random_string(72)
                    user.save()
                    return redirect(reverse('login-page'))
                else:
                    activate_form.add_error('email_active_code', 'کد واردشده اشتباه می باشد')
            else:
                raise Http404
        context = {
            'activate_form': activate_form,
            'email_active_url': email_active_url
        }
        return render(request, 'account_module/email_authenticate.html', context)


class Login(View):
    def get(self, request: HttpRequest):
        if request.user.is_authenticated:
            return redirect(reverse('home_page'))
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/sign-in.html', context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_password = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'حساب کاربری شما فعال نشده است')
                    send_email('فعالسازی حساب کاربری', user.email, {'user': user}, 'email.html')
                    return redirect(reverse('activate_account', args=[user.email_active_url]))
                else:
                    is_password_correct = user.check_password(user_password)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('password', 'کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'کاربری با مشخصات واردشده یافت نشد')
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/sign-in.html', context)


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_pass_form = ForgotPassword()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'account_module/forget_pass.html', context)

    def post(self, request: HttpRequest):
        forget_pass_form = ForgotPassword(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    forget_pass_form.add_error('email', 'حساب شما فعالسازی نشده است')
                    context = {
                        'forget_pass_form': forget_pass_form
                    }
                    return render(request, 'account_module/forget_pass.html', context)
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'email.html')
                return redirect(reverse('authenticate_page', args=[user.email_active_url]))
            else:
                forget_pass_form.add_error('email', 'ایمیل وارد شده موجود نمی باشد')
                context = {
                    'forget_pass_form': forget_pass_form,
                }
                return render(request, 'account_module/forget_pass.html', context)
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'account_module/forget_pass.html', context)


class AuthenticateView(View):
    def get(self, request: HttpRequest, email_active_url):
        user: User = User.objects.filter(email_active_url__iexact=email_active_url, is_active=True).first()
        if user is not None:
            authenticate_form = ActivateAccount()
            context = {
                'authenticate_form': authenticate_form,
                'email_active_url': email_active_url
            }
            return render(request, 'account_module/authenticate.html', context)
        else:
            raise Http404

    def post(self, request: HttpRequest, email_active_url):
        authenticate_form = ActivateAccount(request.POST)
        if authenticate_form.is_valid():
            authenticate_code = authenticate_form.cleaned_data.get('email_active_code')
            user: User = User.objects.filter(email_active_url__iexact=email_active_url).first()
            if user.email_active_code == authenticate_code:
                user.email_active_code = str(random.randrange(100000, 999999))
                user.email_active_url = get_random_string(72)
                user.save()
                return redirect(reverse('reset_pass_page', args=[user.email_active_url]))
            else:
                authenticate_form.add_error('email_active_code', 'رمز واردشده نادرست است')
        context = {
            'authenticate_form': authenticate_form,
            'email_active_url': email_active_url
        }
        return render(request, 'account_module/authenticate.html', context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, email_active_url):
        user: User = User.objects.filter(email_active_url__iexact=email_active_url).first()
        if user is not None:
            reset_pass = ResetPassword()
            context = {
                'reset_pass': reset_pass,
                'email_active_url': email_active_url
            }
            return render(request, 'account_module/reset_pass.html', context)
        else:
            raise Http404

    def post(self, request: HttpRequest, email_active_url):
        reset_pass = ResetPassword(request.POST)
        user: User = User.objects.filter(email_active_url__iexact=email_active_url).first()
        if reset_pass.is_valid():
            if user is None:
                raise Http404
            user_new_pass = reset_pass.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = str(random.randrange(100000, 999999))
            user.email_active_url = get_random_string(72)
            user.save()
            return redirect(reverse('login-page'))
        context = {
            'reset_pass': reset_pass,
            'email_active_url': email_active_url
        }
        return render(request, 'account_module/reset_pass.html', context)


def logout_user(request: HttpRequest):
    logout(request)
    return redirect(reverse('home_page'))
