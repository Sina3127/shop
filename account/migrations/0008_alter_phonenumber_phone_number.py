# Generated by Django 3.2 on 2022-12-22 05:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_phonenumber_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='phone_number',
            field=models.IntegerField(unique=True, validators=[django.core.validators.MaxValueValidator(999999999999)]),
        ),
    ]
