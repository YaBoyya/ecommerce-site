# Generated by Django 4.2.7 on 2024-02-22 11:14

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='total',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Modified at'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='modified_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Modified at'),
        ),
    ]
