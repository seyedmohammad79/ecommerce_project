from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.Login.as_view(), name='login-page'),
    path('sign-up/', views.SignUp.as_view(), name='sign-up-page'),
    path('activate-account/<email_active_url>', views.ActivateUserView.as_view(), name='activate_account'),
    path('forget-password', views.ForgetPasswordView.as_view(), name='forget_password_page'),
    path('authenticate/<email_active_url>', views.AuthenticateView.as_view(), name='authenticate_page'),
    path('reset-password/<email_active_url>', views.ResetPasswordView.as_view(), name='reset_pass_page'),
    path('logout/', views.logout_user, name='logout_page'),
]
