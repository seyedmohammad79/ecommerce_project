from django.db.models import Max, Count
from django.http import HttpRequest
from django.shortcuts import render
from django.views import View

from product_module.models import Product

import datetime

from utils.email_service import send_email


# Create your views here.


class HomePage(View):
    def get(self, request: HttpRequest):
        send_email('فعالسازی حساب کاربری', 'hosseiniseyedmohammad3@gmail.com', {}, 'email.html')
        products = Product.objects.filter(is_active=True, time__gt=datetime.datetime.now().replace(microsecond=0)).annotate(suggest_count=Count("auctionproduct"))[:4]
        context = {
            'products': products
        }
        return render(request, 'home_module/home_page.html', context)

    def post(self, request: HttpRequest):
        pass
