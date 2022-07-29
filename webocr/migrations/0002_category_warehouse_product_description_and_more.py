# Generated by Django 4.0.6 on 2022-07-13 23:02

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('webocr', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='warehouse',
            field=models.CharField(default='Not Available', max_length=200),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(choices=[('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec')], default='Windsor', max_length=2),
        ),
        migrations.AlterField(
            model_name='client',
            name='company',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_units', models.PositiveIntegerField()),
                ('order_status', models.IntegerField(choices=[(0, 'Order Cancelled'), (1, 'Order Placed'), (2, 'Order Shipped'), (3, 'Order Delivered')], default=1)),
                ('status_date', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clients', to='webocr.client')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='webocr.product')),
            ],
        ),
    ]