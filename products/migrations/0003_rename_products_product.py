# Generated by Django 5.0.4 on 2024-09-21 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_products_delete_product'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]