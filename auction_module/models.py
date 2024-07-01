from django.db import models
from jalali_date import datetime2jalali, date2jalali

from account_module.models import User
from product_module.models import Product


# Create your models here.

class AuctionProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    time_auction = models.DateTimeField(auto_now_add=True, verbose_name='زمان پیشنهاد')
    price = models.IntegerField(verbose_name='قیمت پیشنهادی')

    class Meta:
        verbose_name = 'پشنهاد حراجی ها'
        verbose_name_plural = 'پیشنهادهای حراجی ها'

    def get_jalali_date(self):
        return datetime2jalali(self.time_auction).strftime('%m/%d ، %H:%M')

    def date_jalali(self):
        return date2jalali(self.time_auction)

    def time_jalali(self):
        return datetime2jalali(self.time_auction).strftime('%H:%M')

    def __str__(self):
        return str(self.user)

