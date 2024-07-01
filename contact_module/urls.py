from django.urls import path
from . import views
urlpatterns = [
    path('about-us/', views.about_us, name='about_us_page'),
    path('contact-us/', views.ContactUsView.as_view(), name='contact_us_page'),
    path('faqs/', views.faqs_page, name='faqs_page'),
]
