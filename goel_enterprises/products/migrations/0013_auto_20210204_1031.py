# Generated by Django 2.2 on 2021-02-04 10:31

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_auto_20210204_1019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=products.models.upload_image_path),
        ),
    ]
