# Generated by Django 4.0.6 on 2022-07-13 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webocr', '0002_category_warehouse_product_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='province',
            field=models.CharField(choices=[('AB', 'Alberta'), ('MB', 'Manitoba'), ('ON', 'Ontario'), ('QC', 'Quebec')], default='ON', max_length=2),
        ),
        migrations.AlterField(
            model_name='client',
            name='city',
            field=models.CharField(default='Windsor', max_length=20),
        ),
    ]