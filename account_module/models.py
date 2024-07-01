from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    image = models.ImageField(upload_to='images/profile', verbose_name='تصویر پروفایل')
    email_active_code = models.CharField(max_length=6, verbose_name='کد فعالسازی', default='100000')
    email_active_url = models.CharField(max_length=100, db_index=True, verbose_name='url فعالسازی ایمیل')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name != '' and self.last_name != '':
            return self.get_full_name()
        return self.email
