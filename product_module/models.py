from django.db import models
from jalali_date import datetime2jalali

from account_module.models import User


# Create your models here.


class ProductCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name='نام دسته')
    url_title = models.CharField(max_length=200, db_index=True, verbose_name='عنوان در url')
    image = models.FileField(upload_to='images/category', verbose_name='تصویر دسته', null=True)
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'دسته'
        verbose_name_plural = 'دسته ها'

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان محصول')
    Image = models.ImageField(upload_to='images/products', verbose_name='تصویر محصول')
    category = models.ForeignKey(ProductCategory, null=True, blank=True, on_delete=models.CASCADE, verbose_name='دسته محصول')
    start_price = models.IntegerField(verbose_name='قیمت ابتدایی')
    end_price = models.IntegerField(null=True, verbose_name='قیمت نهایی')
    description = models.TextField(verbose_name='توضیحات محصول')
    time = models.DateTimeField(verbose_name='مدت زمان حراجی')
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, db_index=True, verbose_name='کابر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def get_jalali_date(self):
        return datetime2jalali(self.time).strftime('%y/%m/%d ، %H:%M')

    def find_max_suggest(self):
        suggest = list(self.auctionproduct_set.all())
        max_suggest = max(suggest, key=lambda x: x.price)
        return max_suggest

    def __str__(self):
        return self.title


class ProductVisit(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, verbose_name='کاربر', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.title} / {self.ip}'

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدیدهای محصول'
