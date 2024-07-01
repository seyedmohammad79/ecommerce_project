from django import forms

from product_module.models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'Image', 'start_price', 'end_price', 'category', 'description', 'time']
        widgets = {
            'title': forms.TextInput(attrs={
                'id': 'login-email',
                'placeholder': 'نام محصول'
            }),
            'start_price': forms.NumberInput(attrs={
                'placeholder': 'قیمت ابتدایی'
            }),
            'Image': forms.FileInput(attrs={
                'id': 'image_upload',
                'accept': 'image/*',
                'placeholder': 'تصویر محصول'
            })
            ,
            'end_price': forms.NumberInput(attrs={
                'placeholder': 'قیمت نهایی'
            }),
            'description': forms.Textarea(attrs={
                # 'placeholder': 'توضیحات محصول'
            }),
            'time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'placeholder': 'مدت زمان حراجی'
            }),
            'category': forms.Select(attrs={

            })
        }
