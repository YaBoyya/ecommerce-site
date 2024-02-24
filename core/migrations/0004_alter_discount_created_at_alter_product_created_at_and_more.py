# Generated by Django 4.2.7 on 2024-02-22 11:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_remove_discount_active_discount_is_active_and_more_squashed_0003_alter_discount_deleted_at_alter_discount_modified_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=5, verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='productcategory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
        migrations.AlterField(
            model_name='productinventory',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='Created at'),
        ),
    ]