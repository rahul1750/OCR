# Generated by Django 4.0.6 on 2022-07-20 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webocr', '0003_client_province_alter_client_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='intrested',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
