from django.contrib.auth.decorators import login_required
from django.db.models import Max, Count
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from auction_module.models import AuctionProduct
from product_module.forms import ProductForm
from product_module.models import Product, ProductVisit
from utils.http_service import get_client_ip


# Create your views here.
@method_decorator(login_required, name='dispatch')
class CreateProduct(View):
    def get(self, request: HttpRequest):
        product_form = ProductForm()
        context = {
            'product_form': product_form
        }
        return render(request, 'product_module/create_product.html', context)

    def post(self, request: HttpRequest):
        product_form = ProductForm(request.POST, request.FILES)
        message = str()
        if product_form.is_valid():
            product: Product = Product.objects.filter(user_id=request.user.id, is_active=True).exists()
            if not product:
                p = product_form.cleaned_data
                new_product = Product(title=p['title'], Image=request.FILES['Image'],
                                      category=p['category'], start_price=p['start_price'],
                                      end_price=p['end_price'], description=p['description'],
                                      time=p['time'], user_id=request.user.id, is_active=True)
                new_product.save()
                return redirect(reverse('home_page'))
            else:
                message = 'شما محصول فعال در حراجی دارید'
        else:
            message = 'اطلاعات فرم به اشتباه وارد شده است'

        context = {
            'product_form': product_form,
            'status': 'error',
            'title': '',
            'text': message,
            'icon': 'error',
            'confirmButtonColor': "#3085d6",
            'confirmButtonText': "تأیید"
        }
        return render(request, 'product_module/create_product.html', context)


class ProductDetail(View):
    def get(self, request: HttpRequest, product_id):
        product: Product = Product.objects.filter(id=product_id).annotate(visit_count=Count("productvisit")).first()
        if product is None:
            raise Http404
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=product_id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=product_id)
            new_visit.save()
        t = int(round(product.time.timestamp())*1000)
        max_price = AuctionProduct.objects.filter(product_id=product_id).aggregate(Max('price', default=product.start_price))
        suggests = AuctionProduct.objects.filter(product_id=product_id).order_by('-price')
        suggest_count = AuctionProduct.objects.filter(product_id=product_id).count()
        context = {
            'product': product,
            'timer': t,
            'max_price': max_price['price__max'],
            'suggests': suggests,
            'suggest_count': suggest_count
        }
        return render(request, 'product_module/product_detail.html', context)

    def post(self, request: HttpRequest, product_id):
        product: Product = Product.objects.filter(id=product_id).annotate(visit_count=Count("productvisit")).first()
        max_price = AuctionProduct.objects.filter(product_id=product_id).aggregate(Max('price', default=product.start_price))
        t = int(round(product.time.timestamp())*1000)
        suggests = AuctionProduct.objects.filter(product_id=product_id).order_by('-price')
        suggest_count = AuctionProduct.objects.filter(product_id=product_id).count()
        if not request.user.is_authenticated:
            context = {
                'product': product,
                'timer': t,
                'max_price': max_price['price__max'],
                'suggests': suggests,
                'suggest_count': suggest_count,
                'status': 'error',
                'text': 'ّبرای پیشنهاد قیمت باید وارد شوید.',
                'icon': 'error',
                'confirmButtonColor': "#3085d6",
                'confirmButtonText': "تأیید"
            }
            return render(request, 'product_module/product_detail.html', context)
        if not request.POST.get('suggest_price').isnumeric():
            context = {
                'product': product,
                'timer': t,
                'max_price': max_price['price__max'],
                'suggests': suggests,
                'suggest_count': suggest_count,
                'status': 'error',
                'text': 'مقدار واردشده نامعتبر است.',
                'icon': 'error',
                'confirmButtonColor': "#3085d6",
                'confirmButtonText': "تأیید"
            }
            return render(request, 'product_module/product_detail.html', context)
        suggest_price = int(request.POST.get('suggest_price'))
        if suggest_price <= max_price['price__max']:
            context = {
                'product': product,
                'timer': t,
                'max_price': max_price['price__max'],
                'suggests': suggests,
                'suggest_count': suggest_count,
                'status': 'error',
                'text': 'قیمت پیشنهادی شما از قیمت فعلی پایین تر یا برابر می باشد.',
                'icon': 'error',
                'confirmButtonColor': "#3085d6",
                'confirmButtonText': "تأیید"
            }
            return render(request, 'product_module/product_detail.html', context)
        else:
            new_suggest = AuctionProduct(user_id=request.user.id, product_id=product_id, price=suggest_price)
            new_suggest.save()
            max_price = AuctionProduct.objects.filter(product_id=product_id).aggregate(Max('price', default=product.start_price))
            suggests = AuctionProduct.objects.filter(product_id=product_id).order_by('-price')
            suggest_count = AuctionProduct.objects.filter(product_id=product_id).count()
            context = {
                'product': product,
                'timer': t,
                'max_price': max_price['price__max'],
                'suggests': suggests,
                'suggest_count': suggest_count,
                'status': 'success',
                'text': 'پیشنهاد شما با موفقیت ثبت شد.',
                'icon': 'success',
                'confirmButtonColor': "#3085d6",
                'confirmButtonText': "تأیید"
            }
            return render(request, 'product_module/product_detail.html', context)
