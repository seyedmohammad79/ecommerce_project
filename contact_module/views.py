from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from contact_module.models import ContactUs


# Create your views here.


def about_us(request: HttpRequest):
    return render(request, 'contact_module/about_us.html', {})


class ContactUsView(View):
    def get(self, request: HttpRequest):
        return render(request, 'contact_module/contact_us.html', {})

    def post(self, request: HttpRequest):
        contact_form = request.POST
        full_name = contact_form['full_name']
        email = contact_form['email']
        message = contact_form['message']
        new_message: ContactUs = ContactUs(email=email, full_name=full_name, message=message)
        new_message.save()
        context = {
            'status': 'success',
            'title': '',
            'text': 'پیام شما با موفقیت ثبت شد.',
            'icon': 'success',
            'confirmButtonColor': "#3085d6",
            'confirmButtonText': "تأیید"
        }
        return render(request, 'contact_module/contact_us.html', context)


def faqs_page(request: HttpRequest):
    return render(request, 'contact_module/faq.html', {})
