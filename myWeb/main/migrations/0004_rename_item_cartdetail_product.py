# Generated by Django 4.2 on 2023-05-11 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_cart_cartdetail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartdetail',
            old_name='item',
            new_name='product',
        ),
    ]
