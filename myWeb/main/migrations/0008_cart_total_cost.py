# Generated by Django 4.2 on 2023-05-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_cartdetail_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='total_cost',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
