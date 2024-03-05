# Generated by Django 4.2.7 on 2024-03-05 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0003_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderdetails',
            name='total',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='total'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=9),
        ),
    ]