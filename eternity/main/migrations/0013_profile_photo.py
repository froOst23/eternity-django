# Generated by Django 3.1.1 on 2020-09-30 10:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.FileField(blank=True, null=True, upload_to='', validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])], verbose_name='Изображение'),
        ),
    ]
