# Generated by Django 5.0.6 on 2024-06-05 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("product_module", "0002_alter_productcategory_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="end_price",
            field=models.IntegerField(null=True, verbose_name="قیمت نهایی"),
        ),
    ]
