# Generated by Django 3.2 on 2022-12-11 18:13

from django.db import migrations, models
import shop.validators


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_alter_product_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cover',
            field=models.ImageField(upload_to='uploads/', validators=[shop.validators.validate_minimum_size]),
        ),
    ]
