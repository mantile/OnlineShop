# Generated by Django 5.1.1 on 2024-09-23 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_remove_product_image_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
    ]