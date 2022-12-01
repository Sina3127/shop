# Generated by Django 3.2 on 2022-12-01 04:59

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_merge_0005_auto_20221123_2106_0006_auto_20221129_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cover',
            field=models.ImageField(upload_to='uploads/', validators=[shop.validators.validate_minimum_size]),
        ),
    ]
